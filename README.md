# Do Yelp Friends Influence Reviews?

This is a capstone project for the Johns Hopkins Data Science specialization on Coursera.
Intent is to use the datasets provided by the Yelp Dataset Challenge to uncover interesting
features of the data.

This particular project is aimed at attempting to process the *relational* structure of the
datasets, using a relational database for as much as possible of the computation.  It is
also an attempt to wrestle together multiple languages under the R knitr document framework.
Here, there's an unholy mixture of bash, Python, SQL, and R.

If you would like to run this code, you'll need the following:

* R and RStudio
* MySQL, preferably at least v 5.7, and the Python-MySQL connector (both from Oracle)
* Python 2.7
* Assorted R and Python packages, which will announce their lack by causing the code to fail,
  at which point, you can install them.

But beware:

* This will take a long time, perhaps 12 hours, to complete.
* You should not blindly run stuff you find on the Internet.

If you would prefer to *not* run this code, but just see the result, look at yelp_friend_analysis_report.pdf.

To run this:

* Clone this repository.
* Create a subdirectory within it called data.
* Download the Yelp Challenge data from http://www.yelp.com/dataset_challenge into the data subdirectory.
* Copy the file my-template.cnf to my.cnf. Edit it and replace change\*this\*dummy\*password and
  put\*username\*here. In the [client] section, you'll need your actual MySQL root password. In the
  [clientjhu_datasci_capstone_yelp] section, pick a username and password for this project's
  database, which will be called jhu_datasci_capstone_yelp.
* Start the MySQL server with the option local_infile=1 (see comments in the Rmd file about this).
* In RStudio, set the working directory to the repository.
* Open yelp_friend_analysis_report.Rmd
* Poke knit to PDF.

NOTE: All of the former stand-alone scripts have been converted to code chunks in the Rmd file.
Next step is testing to make sure nothing broke during conversion. Re-running the entire process
from the ground up will take about a day.