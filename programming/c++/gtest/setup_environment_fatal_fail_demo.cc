#include <gtest/gtest.h>

class SetupEnvironment : public testing::Environment {
public:
  void SetUp() override {
    GTEST_FAIL() << "Calling a fatal failure";
  }
};

TEST(Test, AlwaysPasses) {
  EXPECT_EQ(true, true);
}

TEST(Test, AlwaysFails) {
  EXPECT_EQ(true, false);
}

int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);

  testing::AddGlobalTestEnvironment(new SetupEnvironment());

  return (RUN_ALL_TESTS());
}
