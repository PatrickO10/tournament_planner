# Tournament Planner
=============
## About:
The objective of this program is to manage a swiss style tournament.

Functionalities:
1. Allows player registration and the player's name doesn't have to be unique.
2. Allows matches to be registered.
3. Allows standings to be reported.
4. Allows pairing for the next round.

### Installation

1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
2. Clone the [tournament_planner](https://github.com/PatrickO10/tournament_planner.git) repository
3. Launch the Vagrant VM
4. In command line cd into tournament_planner/vagrant

	`cd tournament_planner/vagrant`


5. Launch Vagrant VM by typing vagrant up and then followed by vagrant ssh.

6. Now, cd to the tournament directory:

	`cd /vagrant/tournament`

7. Next, import the file that will create the database schema.
	You can either type this in the command line:

		`psql -f tournament.sql`

 	or type psql and hit enter and then type \i tournament.sql

		`psql`

		`\i tournament.sql`

 	To leave type psql type
 		`\q`

8. Now you can test by typing in the command line:
	`python tournament_test.py`

