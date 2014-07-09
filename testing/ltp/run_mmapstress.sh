#!/bin/sh

random_offset()
{
	local filesystem_high_watermark=$(( 9 * $(df -k . | awk 'NR > 1 { print $4 }') * 1024 / 10 / 8 ))

	python2 -c "import random, sys
sys.stdout.write(str(0.75 * random.randrange($filesystem_high_watermark)))
"
}

random_size()
{
	local filesystem_high_watermark=$(( $(df -k . | awk 'NR > 1 { print $4 }') * 1024 ))

	python2 -c "import random, sys
sys.stdout.write(str(random.randrange(1, $filesystem_high_watermark)))
"
}

random_time()
{
	python2 -c "import random, sys
sys.stdout.write(str(random.randrange(10)))
"
}

for standalone in mmap-corruption01 mmapstress02 mmapstress03 mmapstress08; do
	./$standalone
done

./mmapstress01 -p $(sysctl -n kern.smp.cpus) -t $(random_time) -f $(random_size)
./mmapstress04 $(mktemp -u) $(random_offset)
