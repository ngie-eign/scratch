#include <gtest/gtest.h>

class SetupEnvironment : public ::testing::Environment
{
public:
  void SetUp() { EXPECT_EQ(false, true); };
};

TEST(Test, AlwaysPasses) {
  EXPECT_EQ(true, true);
}

int
main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  testing::AddGlobalTestEnvironment(new SetupEnvironment());
  return RUN_ALL_TESTS();
}
