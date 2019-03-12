#include <iostream>
#include <gtest/gtest.h>

TEST(PassFailTest, Passes) {
  EXPECT_EQ(true, true);
}
TEST(PassFailTest, PassesWithReason) {
  std::cout << "This is a reason" << std::endl;
  EXPECT_EQ(true, true);
}
TEST(PassFailTest, Fails) {
  EXPECT_EQ(false, true);
}
int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
