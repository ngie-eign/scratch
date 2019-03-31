// Copyright 2005, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// The purpose of this file is to generate Google Test output under
// various conditions.  The output will then be verified by
// googletest-output-test.py to ensure that Google Test generates the
// desired messages.  Therefore, most tests in this file are MEANT TO
// FAIL.

// This was shamelessly ripped from
// `googletest/test/googletest-output-test_.cc`; hence the original copyright
// is left intact.

#include <gtest/gtest-spi.h>
#include <gtest/gtest.h>

using testing::Types;

template <typename T>
class TypedTest : public testing::Test {
};

TYPED_TEST_SUITE(TypedTest, testing::Types<int>);

TYPED_TEST(TypedTest, Success) {
  EXPECT_EQ(0, TypeParam());
}

TYPED_TEST(TypedTest, Failure) {
  EXPECT_EQ(1, TypeParam()) << "Expected failure";
}

typedef testing::Types<char, int> TypesForTestWithNames;

template <typename T>
class TypedTestWithNames : public testing::Test {};

class TypedTestNames {
 public:
  template <typename T>
  static std::string GetName(int i) {
    if (testing::internal::IsSame<T, char>::value)
      return std::string("char") + ::testing::PrintToString(i);
    if (testing::internal::IsSame<T, int>::value)
      return std::string("int") + ::testing::PrintToString(i);
  }
};

TYPED_TEST_SUITE(TypedTestWithNames, TypesForTestWithNames, TypedTestNames);

TYPED_TEST(TypedTestWithNames, Success) {}

TYPED_TEST(TypedTestWithNames, Failure) { FAIL(); }

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
