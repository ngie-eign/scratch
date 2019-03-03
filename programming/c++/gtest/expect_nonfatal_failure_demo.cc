#include <gtest/gtest.h>
#include <gtest/gtest-spi.h>

class TestClass {
public:
  bool always_false() const {
    return false;
  }
};
void call_that_fails() {
  TestClass test_obj;
  EXPECT_EQ(test_obj.always_false(), true);
}
class FailingTest : public ::testing::Test { };
TEST_F(FailingTest, AlwaysFails) {
  EXPECT_NONFATAL_FAILURE(call_that_fails(), "");
  EXPECT_NONFATAL_FAILURE({ call_that_fails(); }, "");
}
int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
