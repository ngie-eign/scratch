#include <gtest/gtest.h>

using ::testing::Test;

TEST(SkipTest, AlwaysSkips) {
  GTEST_SKIP() << "this is a skip demo";
}
