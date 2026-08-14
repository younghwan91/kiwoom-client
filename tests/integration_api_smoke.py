#!/usr/bin/env python3
"""실 서버(기본: 모의투자) 대상 조회 API 스모크 테스트 하네스.

모든 '조회' 계열 API 함수를 실제로 호출하고 아웃풋을 검증/리포트한다.
주문/매매(order, credit_order) 및 WebSocket(condition_search)은 제외한다.

사용법:
    # .env 에 KIWOOM_APP_KEY / KIWOOM_APP_SECRET 입력 후
    python tests/integration_api_smoke.py            # 모의투자 서버
    python tests/integration_api_smoke.py --prod     # 실서버
    python tests/integration_api_smoke.py --only stock_info,market

결과:
    - 콘솔에 모듈별 요약/상세 출력
    - tests/integration_report.json 에 전체 결과 저장
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# src 레이아웃 import 가능하게
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from kiwoom_rest_api import KiwoomAPI  # noqa: E402
from kiwoom_rest_api.base import BaseClient, KiwoomAPIError  # noqa: E402

# --- 테스트 기준 상수 -------------------------------------------------------
STK = "005930"            # 삼성전자
ETF_STK = "069500"        # KODEX 200
SECTOR = "001"            # 종합(KOSPI)
TODAY = time.strftime("%Y%m%d")
START = time.strftime("%Y%m%d", time.localtime(time.time() - 14 * 86400))

# 조회 대상 모듈 (주문/신용주문/조건검색 제외)
READONLY_MODULES = [
    "account", "stock_info", "market", "chart", "ranking",
    "sector", "foreign_institution", "short_selling", "slb",
    "theme", "elw", "etf",
]

# api_id 별 호출 파라미터. 없으면 RESOURCE_URL 기반 기본값 사용.
PARAMS: dict[str, dict[str, Any]] = {
    # stock_info
    "ka10001": {"stk_cd": STK},
    "ka10002": {"stk_cd": STK},
    "ka10003": {"stk_cd": STK},
    "ka10013": {"stk_cd": STK, "dt": "1", "qry_tp": "1"},
    "ka10015": {"stk_cd": STK, "strt_dt": START},
    "ka10016": {"mrkt_tp": "000", "ntl_tp": "1", "high_low_close_tp": "1", "stk_cnd": "0",
                 "trde_qty_tp": "00000", "crd_cnd": "0", "updown_incls": "1", "dt": "5", "stex_tp": "3"},
    "ka10017": {"mrkt_tp": "000", "updown_tp": "1", "sort_tp": "1", "stk_cnd": "0",
                 "trde_qty_tp": "00000", "crd_cnd": "0", "trde_gold_tp": "0", "stex_tp": "3"},
    "ka10018": {"high_low_tp": "1", "alacc_rt": "05", "mrkt_tp": "000", "trde_qty_tp": "00000",
                 "stk_cnd": "0", "crd_cnd": "0", "stex_tp": "3"},
    "ka10019": {"mrkt_tp": "000", "flu_tp": "1", "tm_tp": "1", "tm": "60", "trde_qty_tp": "00000",
                 "stk_cnd": "0", "crd_cnd": "0", "pric_cnd": "0", "updown_incls": "1", "stex_tp": "3"},
    "ka10024": {"mrkt_tp": "000", "cycle_tp": "5", "trde_qty_tp": "5", "stex_tp": "3"},
    "ka10025": {"mrkt_tp": "000", "prps_cnctr_rt": "50", "cur_prc_entry": "0",
                 "prpscnt": "10", "cycle_tp": "100", "stex_tp": "3"},
    "ka10026": {"pertp": "1", "stk_cd": STK, "stex_tp": "3"},
    "ka10028": {"sort_tp": "1", "trde_qty_cnd": "0000", "mrkt_tp": "000", "updown_incls": "1",
                 "stk_cnd": "0", "crd_cnd": "0", "trde_prica_cnd": "0", "flu_cnd": "1", "stex_tp": "3"},
    "ka10043": {"stk_cd": STK, "strt_dt": START, "end_dt": TODAY, "qry_dt_tp": "0",
                 "pot_tp": "0", "dt": "5", "sort_base": "1", "mmcm_cd": "001", "stex_tp": "3"},
    "ka10052": {"mmcm_cd": "001", "stk_cd": STK, "mrkt_tp": "0", "qty_tp": "0", "pric_tp": "0", "stex_tp": "3"},
    "ka10054": {"mrkt_tp": "000", "bf_mkrt_tp": "0", "stk_cd": "", "motn_tp": "0", "skip_stk": "000000000",
                 "trde_qty_tp": "0", "min_trde_qty": "0", "max_trde_qty": "0", "trde_prica_tp": "0",
                 "min_trde_prica": "0", "max_trde_prica": "0", "motn_drc": "0", "stex_tp": "3"},
    "ka10055": {"stk_cd": STK, "tdy_pred": "1"},
    "ka10058": {"strt_dt": START, "end_dt": TODAY, "trde_tp": "2", "mrkt_tp": "001", "invsr_tp": "8000", "stex_tp": "3"},
    "ka10059": {"dt": TODAY, "stk_cd": STK, "amt_qty_tp": "1", "trde_tp": "0", "unit_tp": "1000"},
    "ka10061": {"stk_cd": STK, "strt_dt": START, "end_dt": TODAY, "amt_qty_tp": "1", "trde_tp": "0", "unit_tp": "1000"},
    "ka10084": {"stk_cd": STK, "tdy_pred": "1", "tic_min": "0", "strt_dt": START, "end_dt": TODAY},
    "ka10095": {"stk_cd": STK},
    "ka10099": {"mrkt_tp": "0"},
    # (ka00198 needs qry_tp)
    "ka10100": {"stk_cd": STK},
    "ka10101": {"mrkt_tp": "0"},
    "ka10102": {},
    "ka90003": {"trde_upper_tp": "1", "amt_qty_tp": "1", "mrkt_tp": "P00101", "stex_tp": "3"},
    "ka90004": {"dt": TODAY, "mrkt_tp": "P00101", "stex_tp": "3"},
    "ka00198": {"qry_tp": "1"},
    "kt20016": {"mrkt_tp": "000", "mrkt_deal_tp": "000"},
    "kt20017": {"stk_cd": STK},
    # market (mrkcond)
    "ka10004": {"stk_cd": STK},
    "ka10005": {"stk_cd": STK},
    "ka10006": {"stk_cd": STK},
    "ka10007": {"stk_cd": STK},
    "ka10011": {"newstk_recvrht_tp": "00"},
    "ka10044": {"strt_dt": START, "end_dt": TODAY, "trde_tp": "1", "mrkt_tp": "001", "stex_tp": "3"},
    "ka10045": {"stk_cd": STK, "strt_dt": START, "end_dt": TODAY, "orgn_prsm_unp_tp": "0",
                 "for_prsm_unp_tp": "0"},
    "ka10046": {"stk_cd": STK},
    "ka10047": {"stk_cd": STK},
    "ka10063": {"mrkt_tp": "000", "amt_qty_tp": "1", "invsr": "6", "frgn_all": "1", "smtm_netprps_tp": "1",
                 "stex_tp": "3"},
    "ka10066": {"mrkt_tp": "000", "amt_qty_tp": "1", "trde_tp": "0", "stex_tp": "3"},
    "ka10078": {"mmcm_cd": "001", "stk_cd": STK, "strt_dt": START, "end_dt": TODAY},
    "ka10086": {"stk_cd": STK, "qry_dt": TODAY, "indc_tp": "0"},
    "ka10087": {"stk_cd": STK},
    "ka90005": {"date": TODAY, "amt_qty_tp": "1", "mrkt_tp": "P00101", "min_tic_tp": "1", "stex_tp": "3"},
    "ka90006": {"date": TODAY, "amt_qty_tp": "1", "mrkt_tp": "P00101", "min_tic_tp": "1", "stex_tp": "3"},
    "ka90007": {"date": TODAY, "amt_qty_tp": "1", "mrkt_tp": "P00101", "min_tic_tp": "1", "stex_tp": "3"},
    "ka90008": {"stk_cd": STK, "date": TODAY, "amt_qty_tp": "1", "mrkt_tp": "P00101", "min_tic_tp": "1", "stex_tp": "3"},
    "ka90010": {"date": TODAY, "amt_qty_tp": "1", "mrkt_tp": "P00101", "min_tic_tp": "1", "stex_tp": "3"},
    "ka90013": {"stk_cd": STK, "date": TODAY, "amt_qty_tp": "1", "mrkt_tp": "P00101"},
    # chart
    "ka10060": {"dt": TODAY, "stk_cd": STK, "amt_qty_tp": "1", "trde_tp": "0", "unit_tp": "1000"},
    "ka10064": {"mrkt_tp": "000", "amt_qty_tp": "1", "trde_tp": "0", "stk_cd": STK},
    "ka10079": {"stk_cd": STK, "tic_scope": "1", "upd_stkpc_tp": "1"},
    "ka10080": {"stk_cd": STK, "tic_scope": "1", "upd_stkpc_tp": "1"},
    "ka10081": {"stk_cd": STK, "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka10082": {"stk_cd": STK, "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka10083": {"stk_cd": STK, "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka10094": {"stk_cd": STK, "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka20004": {"inds_cd": SECTOR, "tic_scope": "1"},
    "ka20005": {"inds_cd": SECTOR, "tic_scope": "5"},
    "ka20006": {"inds_cd": SECTOR, "base_dt": TODAY},
    "ka20007": {"inds_cd": SECTOR, "base_dt": TODAY},
    "ka20008": {"inds_cd": SECTOR, "base_dt": TODAY},
    "ka20019": {"inds_cd": SECTOR, "base_dt": TODAY},
    # chart - gold spot
    "ka50079": {"stk_cd": "04020000", "tic_scope": "1", "upd_stkpc_tp": "1"},
    "ka50080": {"stk_cd": "04020000", "tic_scope": "1", "upd_stkpc_tp": "1"},
    "ka50081": {"stk_cd": "04020000", "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka50082": {"stk_cd": "04020000", "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka50083": {"stk_cd": "04020000", "base_dt": TODAY, "upd_stkpc_tp": "1"},
    "ka50091": {"stk_cd": "04020000", "tic_scope": "1", "upd_stkpc_tp": "1"},
    "ka50092": {"stk_cd": "04020000", "tic_scope": "1", "upd_stkpc_tp": "1"},
    # ranking (rkinfo)
    "ka10020": {"mrkt_tp": "001", "sort_tp": "1", "trde_qty_tp": "0000", "stk_cnd": "0", "crd_cnd": "0", "stex_tp": "3"},
    "ka10021": {"mrkt_tp": "001", "trde_tp": "1", "sort_tp": "1", "tm_tp": "30", "trde_qty_tp": "1",
                 "stk_cnd": "0", "stex_tp": "3"},
    "ka10022": {"mrkt_tp": "001", "rt_tp": "1", "tm_tp": "1", "trde_qty_tp": "5", "stk_cnd": "0", "stex_tp": "3"},
    "ka10023": {"mrkt_tp": "000", "sort_tp": "1", "tm_tp": "2", "trde_qty_tp": "5", "tm": "60",
                 "stk_cnd": "0", "pric_tp": "0", "stex_tp": "3"},
    "ka10027": {"mrkt_tp": "000", "sort_tp": "1", "trde_qty_cnd": "0000", "stk_cnd": "0", "crd_cnd": "0",
                 "updown_incls": "1", "pric_cnd": "0", "trde_prica_cnd": "0", "stex_tp": "3"},
    "ka10029": {"mrkt_tp": "000", "sort_tp": "1", "trde_qty_cnd": "0", "stk_cnd": "0", "crd_cnd": "0",
                 "pric_cnd": "0", "stex_tp": "3"},
    "ka10030": {"mrkt_tp": "000", "sort_tp": "1", "mang_stk_incls": "0", "crd_tp": "0", "trde_qty_tp": "0",
                 "pric_tp": "0", "trde_prica_tp": "0", "mrkt_open_tp": "0", "stex_tp": "3"},
    "ka10031": {"mrkt_tp": "000", "qry_tp": "1", "rank_strt": "0", "rank_end": "10", "stex_tp": "3"},
    "ka10032": {"mrkt_tp": "000", "mang_stk_incls": "0", "stex_tp": "3"},
    "ka10033": {"mrkt_tp": "000", "trde_qty_tp": "0", "stk_cnd": "0", "updown_incls": "1", "crd_cnd": "0", "stex_tp": "3"},
    "ka10034": {"mrkt_tp": "000", "trde_tp": "2", "dt": "0", "stex_tp": "3"},
    "ka10035": {"mrkt_tp": "000", "trde_tp": "2", "base_dt_tp": "1", "stex_tp": "3"},
    "ka10036": {"mrkt_tp": "000", "dt": "0", "stex_tp": "3"},
    "ka10037": {"mrkt_tp": "000", "dt": "0", "trde_tp": "1", "sort_tp": "2", "stex_tp": "3"},
    "ka10038": {"stk_cd": STK, "strt_dt": START, "end_dt": TODAY, "qry_tp": "1", "dt": "1"},
    "ka10039": {"mmcm_cd": "001", "trde_qty_tp": "0", "trde_tp": "1", "dt": "1", "stex_tp": "3"},
    "ka10040": {"stk_cd": STK},
    "ka10042": {"strt_dt": START, "end_dt": TODAY, "qry_dt_tp": "0", "pot_tp": "0", "dt": "5",
                 "sort_base": "1", "stk_cd": STK, "stex_tp": "3"},
    "ka10053": {"stk_cd": STK},
    "ka10062": {"strt_dt": START, "mrkt_tp": "000", "trde_tp": "1", "sort_cnd": "1", "unit_tp": "1", "stex_tp": "3"},
    "ka10065": {"trde_tp": "1", "mrkt_tp": "000", "orgn_tp": "9000"},
    "ka10098": {"mrkt_tp": "000", "sort_base": "5", "stk_cnd": "0", "trde_qty_cnd": "0",
                 "crd_cnd": "0", "trde_prica": "0"},
    "ka90009": {"mrkt_tp": "000", "amt_qty_tp": "0", "qry_dt_tp": "0", "date": TODAY, "stex_tp": "3"},
    # sector (sect)
    "ka10010": {"stk_cd": STK},
    "ka10051": {"mrkt_tp": "0", "amt_qty_tp": "0", "base_dt": TODAY, "stex_tp": "3"},
    "ka20001": {"mrkt_tp": "0", "inds_cd": SECTOR},
    "ka20002": {"mrkt_tp": "0", "inds_cd": SECTOR, "stex_tp": "3"},
    "ka20003": {"inds_cd": SECTOR},
    "ka20009": {"mrkt_tp": "0", "inds_cd": SECTOR},
    # foreign_institution (frgnistt)
    "ka10008": {"stk_cd": STK},
    "ka10009": {"stk_cd": STK},
    "ka10131": {"dt": "1", "strt_dt": START, "end_dt": TODAY, "mrkt_tp": "001", "netslmt_tp": "2",
                 "stk_inds_tp": "0", "amt_qty_tp": "0", "stex_tp": "3"},
    "ka52301": {"stk_cd": "04020000"},
    # short_selling (shsa)
    "ka10014": {"stk_cd": STK, "tm_tp": "1", "strt_dt": START, "end_dt": TODAY},
    # slb
    "ka10068": {"strt_dt": START, "end_dt": TODAY, "all_tp": "1"},
    "ka10069": {"strt_dt": START, "end_dt": TODAY, "mrkt_tp": "001"},
    "ka20068": {"strt_dt": START, "end_dt": TODAY, "all_tp": "0", "stk_cd": STK},
    "ka90012": {"dt": TODAY, "mrkt_tp": "001"},
    # theme
    "ka90001": {"qry_tp": "0", "date_tp": "10", "flu_pl_amt_tp": "1", "stex_tp": "3"},
    "ka90002": {"date_tp": "2", "thema_grp_cd": "100", "stex_tp": "3"},
    # elw
    "ka10048": {"stk_cd": STK},
    "ka10050": {"stk_cd": STK},
    "ka30001": {"flu_tp": "1", "tm_tp": "2", "tm": "1", "trde_qty_tp": "0", "isscomp_cd": "000000000000",
                 "bsis_aset_cd": "000000000000", "rght_tp": "000", "lpcd": "000000000000", "trde_end_elwskip": "0"},
    "ka30002": {"isscomp_cd": "003", "trde_qty_tp": "0", "trde_tp": "2", "dt": "60", "trde_end_elwskip": "0"},
    "ka30003": {"stk_cd": STK, "bsis_aset_cd": "201", "base_dt": TODAY, "elwccnt": "0"},
    "ka30004": {"isscomp_cd": "000000000000", "bsis_aset_cd": "000000000000", "rght_tp": "000",
                 "lpcd": "000000000000", "trde_end_elwskip": "0"},
    "ka30005": {"isscomp_cd": "000000000000", "bsis_aset_cd": "000000000000", "rght_tp": "0",
                 "lpcd": "000000000000", "sort_tp": "0"},
    "ka30009": {"sort_tp": "1", "rght_tp": "000", "trde_end_skip": "0"},
    "ka30010": {"sort_tp": "1", "rght_tp": "000", "trde_end_skip": "0"},
    "ka30011": {"stk_cd": STK},
    "ka30012": {"stk_cd": STK},
    # etf
    "ka40001": {"stk_cd": ETF_STK, "etfobjt_idex_cd": "207", "dt": "3"},
    "ka40002": {"stk_cd": ETF_STK},
    "ka40003": {"stk_cd": ETF_STK},
    "ka40004": {"txon_type": "0", "navpre": "0", "mngmcomp": "0000", "txon_yn": "0", "trace_idex": "0", "stex_tp": "1"},
    "ka40006": {"stk_cd": ETF_STK},
    "ka40007": {"stk_cd": ETF_STK},
    "ka40008": {"stk_cd": ETF_STK},
    "ka40009": {"stk_cd": ETF_STK},
    "ka40010": {"stk_cd": ETF_STK},
    # account (acnt) — 계좌/잔고/손익 조회
    "ka10072": {"stk_cd": STK, "strt_dt": TODAY},
    "ka10073": {"stk_cd": STK, "strt_dt": START, "end_dt": TODAY},
    "ka10074": {"strt_dt": START, "end_dt": TODAY},
    "ka10075": {"all_stk_tp": "0", "trde_tp": "0", "stk_cd": STK, "stex_tp": "0"},
    "ka10076": {"stk_cd": STK, "qry_tp": "0", "sell_tp": "0", "ord_no": "", "stex_tp": "0"},
    "ka10077": {"stk_cd": STK},
    "ka10085": {"stex_tp": "0"},
    "ka10088": {"ord_no": ""},
    "ka10170": {"base_dt": TODAY, "ottks_tp": "1", "ch_crd_tp": "0"},
    "kt00001": {"qry_tp": "3"},
    "kt00002": {"start_dt": START, "end_dt": TODAY},
    "kt00003": {"qry_tp": "0"},
    "kt00004": {"qry_tp": "0", "dmst_stex_tp": "KRX"},
    "kt00005": {"dmst_stex_tp": "KRX"},
    "kt00007": {"ord_dt": "", "qry_tp": "1", "stk_bond_tp": "0", "sell_tp": "0", "stk_cd": "", "fr_ord_no": "",
                 "dmst_stex_tp": "%"},
    "kt00008": {"strt_dcd_seq": ""},
    "kt00009": {"ord_dt": "", "stk_bond_tp": "0", "mrkt_tp": "0", "sell_tp": "0", "qry_tp": "0",
                 "stk_cd": "", "fr_ord_no": "", "dmst_stex_tp": "KRX"},
    "kt00010": {"stk_cd": STK, "trde_tp": "2", "uv": "0", "trde_qty": "0"},
    "kt00011": {"stk_cd": STK, "uv": "0"},
    "kt00012": {"stk_cd": STK, "uv": "0"},
    "kt00013": {},
    "kt00015": {"strt_dt": START, "end_dt": TODAY, "tp": "0", "stk_cd": "", "crnc_cd": "", "gds_tp": "0",
                 "frgn_stex_code": "", "dmst_stex_tp": "%"},
    "kt00016": {"fr_dt": START, "to_dt": TODAY},
    "kt00017": {},
    "kt00018": {"qry_tp": "1", "dmst_stex_tp": "KRX"},
    "ka00001": {},
    "ka01690": {"qry_dt": TODAY},
    "kt50020": {},
    "kt50021": {},
    "kt50030": {"ord_dt": TODAY, "mrkt_deal_tp": "0", "stk_bond_tp": "0", "sell_tp": "0",
                 "strt_dt": START, "end_dt": TODAY},
    "kt50031": {"ord_dt": TODAY, "qry_tp": "0", "stk_bond_tp": "0", "sell_tp": "0", "mrkt_deal_tp": "0"},
    "kt50032": {"strt_dt": START, "end_dt": TODAY, "ord_dt": TODAY, "qry_tp": "0", "gds_tp": "0",
                 "stk_bond_tp": "0", "mrkt_deal_tp": "0"},
    "kt50075": {"ord_dt": TODAY, "stk_bond_tp": "0", "mrkt_deal_tp": "0"},
    # market gold spot
    "ka50010": {"stk_cd": "04020000"},
    "ka50012": {"stk_cd": "04020000", "base_dt": TODAY},
    "ka50087": {"stk_cd": "04020000"},
    "ka50100": {"stk_cd": "04020000"},
    "ka50101": {"stk_cd": "04020000", "tic_scope": "1"},
}

# RESOURCE_URL 기반 기본 파라미터 (api_id 미등록 시)
RESOURCE_DEFAULTS: dict[str, dict[str, Any]] = {
    "/api/dostk/stkinfo": {"stk_cd": STK},
    "/api/dostk/mrkcond": {"stk_cd": STK},
    "/api/dostk/chart": {"stk_cd": STK},
    "/api/dostk/frgnistt": {"stk_cd": STK},
    "/api/dostk/shsa": {"stk_cd": STK},
}


def discover_methods(api: KiwoomAPI) -> list[tuple[str, str, str, Any]]:
    """(module_name, method_name, api_id, bound_method) 목록을 리플렉션으로 추출."""
    found: list[tuple[str, str, str, Any]] = []
    orig = BaseClient.request
    captured: dict[str, str] = {}

    def spy(self, resource_url, api_id, body=None, cont_yn="N", next_key="", extra_headers=None):
        captured["api_id"] = api_id
        captured["resource_url"] = resource_url
        raise _Stop()

    class _Stop(Exception):
        pass

    BaseClient.request = spy  # type: ignore[method-assign]
    try:
        for mod_name in READONLY_MODULES:
            module = getattr(api, mod_name)
            for meth_name in dir(module):
                if meth_name.startswith("_"):
                    continue
                meth = getattr(module, meth_name)
                if not callable(meth):
                    continue
                captured.clear()
                try:
                    meth()
                except _Stop:
                    pass
                except TypeError:
                    continue  # 시그니처가 다른 비-API 메서드
                api_id = captured.get("api_id")
                resource = captured.get("resource_url", "")
                if api_id:
                    found.append((mod_name, meth_name, api_id, resource))
    finally:
        BaseClient.request = orig  # type: ignore[method-assign]
    return found


def params_for(api_id: str, resource: str) -> dict[str, Any]:
    if api_id in PARAMS:
        return PARAMS[api_id]
    return RESOURCE_DEFAULTS.get(resource, {})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", action="store_true", help="실서버 사용 (기본: 모의투자)")
    parser.add_argument("--only", default="", help="콤마구분 모듈명만 테스트")
    parser.add_argument("--sleep", type=float, default=0.3, help="호출 간 대기(초)")
    args = parser.parse_args()

    app_key = os.environ.get("KIWOOM_APP_KEY", "")
    app_secret = os.environ.get("KIWOOM_APP_SECRET", "")
    # .env 직접 로드 (python-dotenv 없이)
    env_path = ROOT / ".env"
    if (not app_key or app_key == "your_app_key") and env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k.strip() == "KIWOOM_APP_KEY":
                app_key = v
            elif k.strip() == "KIWOOM_APP_SECRET":
                app_secret = v

    if not app_key or app_key == "your_app_key" or not app_secret or app_secret == "your_app_secret":
        print("❌ KIWOOM_APP_KEY / KIWOOM_APP_SECRET 가 .env 또는 환경변수에 설정되지 않았습니다.")
        print("   .env 파일을 열어 실제 발급키를 입력한 뒤 다시 실행하세요.")
        return 2

    is_mock = not args.prod
    server = "모의투자(mockapi)" if is_mock else "실서버(api)"
    only = {m.strip() for m in args.only.split(",") if m.strip()}

    print(f"🔌 서버: {server}")
    api = KiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=is_mock, rate_limit=4.0)

    try:
        tok = api.login()
        if not api._client.access_token:
            print(f"❌ 로그인 실패: {tok}")
            return 1
        print(f"✅ 로그인 성공 (token …{api._client.access_token[-6:]})\n")
    except Exception as e:
        print(f"❌ 로그인 예외: {type(e).__name__}: {e}")
        return 1

    methods = discover_methods(api)
    if only:
        methods = [m for m in methods if m[0] in only]
    print(f"🔎 발견된 조회 API 함수: {len(methods)}개\n")

    results: list[dict[str, Any]] = []
    counts = {"OK": 0, "API_ERROR": 0, "HTTP_ERROR": 0, "EXCEPTION": 0}
    cur_mod = None

    for mod_name, meth_name, api_id, resource in methods:
        if mod_name != cur_mod:
            cur_mod = mod_name
            print(f"── {mod_name} " + "─" * (40 - len(mod_name)))
        params = params_for(api_id, resource)
        module = getattr(api, mod_name)
        meth = getattr(module, meth_name)
        entry: dict[str, Any] = {
            "module": mod_name, "method": meth_name, "api_id": api_id, "params": params,
        }
        try:
            resp = meth(**params)
            rc = resp.get("return_code", 0)
            msg = resp.get("return_msg", "")
            keys = [k for k in resp if k not in ("return_code", "return_msg")]
            entry.update(status="OK", return_code=rc, return_msg=msg, data_keys=keys)
            counts["OK"] += 1
            print(f"  ✅ {meth_name:<34} {api_id}  rc={rc} keys={keys[:4]}")
        except KiwoomAPIError as e:
            entry.update(status="API_ERROR", return_code=e.code, return_msg=e.message)
            counts["API_ERROR"] += 1
            print(f"  ⚠️  {meth_name:<34} {api_id}  rc={e.code} msg={e.message}")
        except Exception as e:
            import httpx
            if isinstance(e, httpx.HTTPStatusError):
                code = e.response.status_code
                body = e.response.text[:200]
                entry.update(status="HTTP_ERROR", http_status=code, body=body)
                counts["HTTP_ERROR"] += 1
                print(f"  ❌ {meth_name:<34} {api_id}  HTTP {code} {body[:80]}")
            else:
                entry.update(status="EXCEPTION", error=f"{type(e).__name__}: {e}")
                counts["EXCEPTION"] += 1
                print(f"  💥 {meth_name:<34} {api_id}  {type(e).__name__}: {e}")
        results.append(entry)
        time.sleep(args.sleep)

    api.close()

    print("\n" + "=" * 56)
    print("📊 요약")
    total = len(results)
    print(f"  전체:       {total}")
    print(f"  ✅ OK:       {counts['OK']}")
    print(f"  ⚠️  API오류:  {counts['API_ERROR']}  (서버 도달 O, 파라미터/시장상태 이슈 가능)")
    print(f"  ❌ HTTP오류: {counts['HTTP_ERROR']}")
    print(f"  💥 예외:     {counts['EXCEPTION']}")

    out = ROOT / "tests" / "integration_report.json"
    out.write_text(json.dumps({"server": server, "counts": counts, "results": results},
                              ensure_ascii=False, indent=2))
    print(f"\n💾 상세 리포트 저장: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
