/**
 * Get the time in time_t using std::chrono interfaces.
 *
 * `std::chrono::system_clock::now()` seems to return the system clock's time,
 * despite the actual timezone not being UTC according to some tests run on
 * FreeBSD.
 *
 * gmtime(..) seems to be the only way to ensure that the time obtained is
 * actually UTC.
 */

#include <cassert>
#include <chrono>
#include <ctime>
#include <iostream>

int
main()
{
	const auto system_tp = std::chrono::system_clock::now();
	const std::time_t system_time = std::chrono::system_clock::to_time_t(system_tp);

	std::cout << "std::chrono::system_clock: " << system_time << " sec" << std::endl;

	// Neither clang 19.x nor gcc 13.x seem to support this pattern.
	// Both toolchains fail when trying to handle `{...}::to_time_t(..)` in
	// different ways.
	//
	// See also: https://lists.isocpp.org/std-discussion/2025/01/2801.php
#if 0
#if __cplusplus >= 202002L
	// Per Microsoft docs, same as `from_sys(system_clock::now())`.
	const auto utc_tp = std::chrono::utc_clock::now();
	const std::time_t utc_time = std::chrono::utc_clock::to_time_t(utc_tp);

	std::cout << "std::chrono::utc_clock: " << utc_time << " sec" << std::endl;
#endif
#endif

	// Note warnings about thread safety in docs.
	std::tm *utc_tm;
	time_t now = time(NULL);
	utc_tm = std::gmtime(&now);
	assert(utc_tm);
	std::time_t utc_time2 = std::mktime(utc_tm);

	std::cout << "gmtime(..): " << utc_time2 << " sec" << std::endl;
}
