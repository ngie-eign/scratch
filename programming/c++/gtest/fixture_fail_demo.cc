#include <gtest/gtest.h>

class SetUpFail : public testing::Test {
public:
  void SetUp() {
    EXPECT_EQ(true, false);
  }
};
class TearDownFail : public testing::Test {
public:
  void TearDown() {
    EXPECT_EQ(true, false);
  }
};

TEST_F(SetUpFail, AlwaysPasses) {
  EXPECT_EQ(true, true);
}

TEST_F(TearDownFail, AlwaysPasses) {
  EXPECT_EQ(true, true);
}

int
main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
