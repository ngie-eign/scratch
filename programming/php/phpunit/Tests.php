<?php
/*
 * A module with some code that's testable.
 */

function foo()
{
	return 3;
}

function fibonacci($x)
{
	if ($x <= 1)
	{
		return (1);
	}
	return ($x * fibonacci($x - 1));
}

class FibTest extends PHPUnit_Framework_TestCase
{
	public function test_basecase_1()
	{
		$this->assertEquals(fibonacci(0), 1);
	}

	public function test_basecase_2()
	{
		$this->assertEquals(fibonacci(1), 1);
	}

	public function test_simplecase_1()
	{
		$this->assertEquals(fibonacci(3), 6);
	}

	public function test_simplecase_2()
	{
		$this->assertEquals(fibonacci(5), 120);
	}

	public function test_larger()
	{
		$this->assertEquals(fibonacci(12), 479001600);
	}
}

class SomethingTest extends PHPUnit_Framework_TestCase
{
	public function test_empty()
	{
		$x = '';
		$this->assertEmpty($x);
	}
}
?>
