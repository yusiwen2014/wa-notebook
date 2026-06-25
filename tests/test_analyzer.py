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
            "CE", "RE_div0", "RE_oob",
            "WA_logic", "WA_code",
            "TLE", "MLE",
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

    def test_re_div0_detection(self):
        code = """
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a / b;
    return 0;
}
        """
        result = analyzer.analyze(code, "RE", "")
        assert result["error_category"] == "RE_div0"

    def test_re_oob_detection(self):
        code = """
#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for(int i=0; i<=n; i++) cin >> a[i];
    return 0;
}
        """
        result = analyzer.analyze(code, "RE", "")
        assert result["error_category"] == "RE_oob"

    def test_wa_logic_vs_code(self):
        # 包含复杂算法关键词 -> 思路错误
        logic_code = """
#include <iostream>
using namespace std;
int dp[1005];
int main() {
    int n; cin >> n;
    dp[0] = 1;
    for(int i=1; i<=n; i++) dp[i] = dp[i-1] * 2;
    cout << dp[n];
    return 0;
}
        """
        result = analyzer.analyze(logic_code, "WA", "DP 计数")
        assert result["error_category"] == "WA_logic"

    def test_tle_detection(self):
        code = """
#include <iostream>
using namespace std;
int main() {
    int n; cin >> n;
    for(int i=0; i<n; i++)
        for(int j=0; j<n; j++) cout << i*j;
    return 0;
}
        """
        result = analyzer.analyze(code, "TLE", "")
        assert result["error_category"] == "TLE"

    def test_mle_detection(self):
        code = """
#include <iostream>
using namespace std;
int a[10000000];
int main() { return 0; }
        """
        result = analyzer.analyze(code, "MLE", "")
        assert result["error_category"] == "MLE"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
