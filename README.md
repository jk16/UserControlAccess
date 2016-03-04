#Practice Project: user access control

###About
* What is a permission?
	* Relation between an operation and a specific thing: (operation, specific)
		* has_permission('viewPage','john') --> true or false
		* john.add_permission('david', 'viewPage') --> john can view davids page

