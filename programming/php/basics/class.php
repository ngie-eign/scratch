<?php
class ParentClass {
	protected $self = array();
	private $self2 = array();

	public function __construct($value = "default") {
		$this->self["value"] = $value;
	}
	public function __get($key) {
		return $this->self[$key];
	}
	public function __set($key, $value) {
		$this->self[$key] = $value;
	}
	public function toString() {
		return get_class($this) . "(".
		     "\$value = \"". $this->value ."\");";
	}
}
class ChildClass extends ParentClass {
	public function __construct($value = "child default",
				    $value2 = "another default") {
		parent::__construct($value = $value);
		$this->self["value2"] = $value2;
	}
	public function toString() {
		return get_class($this) ."(".
		    "\$value = \"". $this->self["value"] ."\", " .
		    "\$value2 = \"". $this->self["value2"] .
		"\");";
	}
}

$po = new ParentClass();
print $po->toString() ."\n";
$po->value = "yarg";
print $po->toString() ."\n";
$po = new ParentClass("foobar");
print $po->toString() ."\n";
$po2 = new ChildClass("foo", "bar");
print $po2->toString() ."\n";
//print $po2->__self2 ."\n";
?>
