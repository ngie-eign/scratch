#include <gtest/gtest.h>

template <class T>
class FooTest : public ::testing::Test {
};

TYPED_TEST_SUITE_P(FooTest);

TYPED_TEST_P(FooTest, HalvingTruncates) {
  TypeParam n = 1;
  EXPECT_EQ(n / 2, 0);
}

TYPED_TEST_P(FooTest, DoublingIsNonzero) {
  TypeParam n = static_cast<TypeParam>(0.25);
  EXPECT_EQ(n * 2, 0);
}

REGISTER_TYPED_TEST_SUITE_P(FooTest,
                            HalvingTruncates, DoublingIsNonzero);

INSTANTIATE_TYPED_TEST_SUITE_P(Integer, FooTest, int);
INSTANTIATE_TYPED_TEST_SUITE_P(Double, FooTest, double);

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
