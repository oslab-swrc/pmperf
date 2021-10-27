## SPDX-FileCopyrightText: Copyright (c) 2021 Electronics and Telecommunications Research Institute
## SPDX-License-Identifier: MIT
## 
## Author : Youngjoo Woo <my.cat.liang@gmail.com>

#!/bin/sh

# mkfs.ext4 -b 4096 -E stride=512 -F /dev/pmem1
# mkfs.ext4 -b 4096 -E stride=512 -F /dev/pmem1.1

#ndctl create-namespace --size 1G -a 2M -r region1

mkdir -p /mnt/pmemfs1.0
mount -o dax /dev/pmem1 /mnt/pmemfs1.0
# dd if=/dev/urandom of=/mnt/pmemfs1.0/data bs=4K count=25288192

for idx in $(seq 27)
do
    mkdir -p /mnt/pmemfs1.${idx}
    mount -o dax /dev/pmem1.${idx} /mnt/pmemfs1.${idx}
    # dd if=/dev/urandom of=/mnt/pmemfs1.${idx}/data bs=4k count=244662
done

mkdir -p /mnt/pmemfs1.28
mount -o dax /dev/pmem1.28 /mnt/pmemfs1.28
# dd if=/dev/urandom of=/mnt/pmemfs1.28/data bs=4K count=25288192