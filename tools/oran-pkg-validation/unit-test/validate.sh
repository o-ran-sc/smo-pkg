#===================================================================
#Copyright © 2020 Aarna Networks, Inc.
#All rights reserved.
#===================================================================
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

#!/bin/sh

echo 
echo "Validating vnf-vsn.csar Unit test case 1"
python3 ../main.py csar-validate -d /tmp/vh2/ --no-verify-cert ../CSAR-dest/vnf-vsn.csar
if [ $? -eq 0 ]
then
	echo "Unit test case 1 Passed"
else
	echo "Unit test case 1 Failed"
fi
echo 
echo "Validating ns-vsn.csar unit test case 2"
echo
python3 ../main.py csar-validate -d /tmp/vh2/ --no-verify-cert ../CSAR-dest/ns-vsn.csar
echo
if [ $? -eq 0 ]
then
	echo "Unit test case 2 Passed"
else
	echo "Unit test case 2 Failed"
fi
echo

