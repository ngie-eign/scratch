#include <gtest/gtest.h>

class TearDownEnvironment : public ::testing::Environment
{
public:
  void TearDown() { EXPECT_EQ(false, true); };
};

TEST(Test, AlwaysPasses) {
  EXPECT_EQ(true, true);
}

int
main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  testing::AddGlobalTestEnvironment(new TearDownEnvironment());
  return RUN_ALL_TESTS();
}
