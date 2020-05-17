from scrapper.plays import show_range


class TestStringMethods:


    def test_should_generate_list_correctly(self):
        low = 1
        high = 12
        nums = [2, 4, 5, 10]
        result = show_range(low, high, nums)

        assert result == [(1, 1), (3, 3), (6, 9), (11, 12)]



