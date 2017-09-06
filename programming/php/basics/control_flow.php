<?php

$i = 0;

$array = array(1, 1.0, 0, -1, 0.1, "0.1");

foreach ($array as $i) {
	if (is_int($i)) {
		print $i ." is an int\n";
	} else {
		print $i ." is not an int\n";
	}
	switch ($i) {
	case "0.1":
		print "\$i matched as '0.1'\n";
		break;
	case 0:
	case 1:
		print "\$i matched as ". $i ."\n";
		break;
	default:
		print $i ." hit the default case\n";
		break;
	}
	switch (true) {
	case ($i < 10):
		print "was less than 10\n";
		break;
	case (is_int($i)):
		print "$i is an int\n";
		break;
	}
}

for ($i = 0; $i < count($array); $i++) {
	print $i ." => ". $array[$i] ."\n";
}

$i = 0;
while ($i < count($array)) {
	print $i ." => ". $array[$i] ."\n";
	$i++;
}

do {
	print "entered while-false 'loop'\n";
} while(false);
print "exited while-false 'loop'\n";

?>
