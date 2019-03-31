#include <gtest/gtest.h>
#include <gtest/gtest-spi.h>

class BarTest : public ::testing::TestWithParam<int> { };

TEST_P(BarTest, IsOdd) {
  EXPECT_NE(GetParam() % 2, 0);
}

TEST_P(BarTest, IsEven) {
  EXPECT_EQ(GetParam() % 2, 0);
}

INSTANTIATE_TEST_SUITE_P(Instance1, BarTest,
                         ::testing::Range(10, 20));
INSTANTIATE_TEST_SUITE_P(Instance2, BarTest,
                         ::testing::Values(1, 6, 10));

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
