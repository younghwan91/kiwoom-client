"""브랜드 색 토큰의 정본 (docs/brand.md "색 토큰" 표와 같다).

그림 생성기(hero_style.py, make_logo.py, make_social.py)가 여기서 색을 가져간다.
matplotlib 같은 의존성 없이 import 된다.
"""

P = {
    "light": dict(
        surface="#ffffff", surface2="#f6f8fa", grid="#e5e7eb",
        ink="#0b0f19", ink2="#4b5563", ink3="#9ca3af",
        blue="#2563EB", amber="#B45309", green="#059669", violet="#7C3AED",
        blue_wash="#2563EB1a", amber_wash="#B453091a", green_wash="#0596691a",
        good="#059669", warn="#B45309", bad="#DC2626",
        seq=["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"],
    ),
    "dark": dict(
        surface="#0d1117", surface2="#161b22", grid="#30363d",
        ink="#e6edf3", ink2="#9da7b3", ink3="#6e7681",
        blue="#3B82F6", amber="#D97706", green="#059669", violet="#8B5CF6",
        blue_wash="#3B82F626", amber_wash="#D9770626", green_wash="#05966926",
        good="#059669", warn="#D97706", bad="#F87171",
        seq=["#0d366b", "#184f95", "#256abf", "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb"],
    ),
}
