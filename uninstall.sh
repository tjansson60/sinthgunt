##############################################################################
#       
#    Copyright 2010 Kaare Hartvig Jensen
#
#    This file is part of sinthgunt.
#
#    yatii is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    yatii is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with yatii.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#sudo python setup.py install --prefix='/usr' --record files.txt
sudo python setup.py install --record files.txt
sudo cat files.txt | sudo xargs rm -rf
rm files.txt
