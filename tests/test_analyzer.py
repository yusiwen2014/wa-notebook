import pytest
from app.services.analyzer import analyzer, ERROR_CATEGORIES


class TestMockAnalyzer:

    def test_analyze_returns_valid_structure(self):
        code = """
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b;
    return 0;
}
        """
        result = analyzer.analyze(code, "WA", "A+B Problem")

        assert "error_category" in result
        assert "error_severity" in result
        assert "error_summary" in result
        assert "error_detail" in result
        assert "suggestion" in result
        assert "hints" in result
        assert isinstance(result["hints"], list)

    def test_all_categories_exist(self):
        expected_cats = [
            "logic_error", "boundary", "overflow", "uninitialized",
            "complexity", "precision", "io_format", "memory",
            "typo", "modular", "graph", "dp",
        ]
        for cat in expected_cats:
            assert cat in ERROR_CATEGORIES
            assert "name" in ERROR_CATEGORIES[cat]
            assert "severity" in ERROR_CATEGORIES[cat]
            assert "hints" in ERROR_CATEGORIES[cat]

    def test_hint_progression(self):
        hints = ["提示1", "提示2", "提示3"]

        h1, idx1 = analyzer.get_next_hint(hints, 0)
        assert h1 == "提示1"
        assert idx1 == 1

        h2, idx2 = analyzer.get_next_hint(hints, 1)
        assert h2 == "提示2"
        assert idx2 == 2

        h3, idx3 = analyzer.get_next_hint(hints, 2)
        assert h3 == "提示3"
        assert idx3 == 3

        h4, idx4 = analyzer.get_next_hint(hints, 3)
        assert "掌握" in h4
        assert idx4 == 3

    def test_overflow_detection(self):
        code = """
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int ans = 0;
    for(int i=1; i<=n; i++) ans += i * i;
    cout << ans << endl;
    return 0;
}
        """
        result = analyzer.analyze(code, "WA", "")
        assert result["error_category"] == "overflow"

    def test_boundary_detection(self):
        code = """
#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for(int i=1; i<=n; i++) cin >> a[i];
    cout << a[n] << endl;
    return 0;
}
        """
        result = analyzer.analyze(code, "WA", "")
        assert result["error_category"] == "boundary"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
