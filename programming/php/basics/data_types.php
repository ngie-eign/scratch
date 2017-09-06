<?php
$list = array("a", "b", "c");
$dict = array(
	1 => "d",
	10 => "f",
	27 => "G",
	"3.5" => 1,
);

$i = 0;
print "LIST::\n";
var_dump($list);
foreach ($list as $value) {
	print "\$list[". $i ."] => ". $value ."\n";
}
print "\nDICT::\n";
var_dump($dict);
foreach (array_keys($dict) as $key) {
	print "\$dict[". $key ."] => ". $dict[$key] ."\n";
}
?>
