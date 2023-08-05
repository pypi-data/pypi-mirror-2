#
#   MailScanner - SMTP E-Mail Virus Scanner
#   Copyright (C) 2002  Julian Field
#
#   $Id: SQLBlackWhiteList.pm,v 1.2 2005/08/19 08:45:34 smfreegard Exp $
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   The author, Julian Field, can be contacted by email at
#      Jules@JulianField.net
#   or by paper mail at
#      Julian Field
#      Dept of Electronics & Computer Science
#      University of Southampton
#      Southampton
#      SO17 1BJ
#      United Kingdom
#

package MailScanner::CustomConfig;

use strict 'vars';
use strict 'refs';
no  strict 'subs'; # Allow bare words for parameter %'s

use vars qw($VERSION);

### The package version, both in 1.23 style *and* usable by MakeMaker:
$VERSION = substr q$Revision: 1.2 $, 10;

use DBI;
my(%Whitelist, %Blacklist);
my($wtime, $btime);
my($refresh_time) = 15;		# Time in minutes before lists are refreshed

#
# Initialise SQL spam whitelist and blacklist
#
sub InitSQLWhitelist {
  MailScanner::Log::InfoLog("Starting up SQL Whitelist");
  my $entries = CreateList('whitelist', \%Whitelist);
  MailScanner::Log::InfoLog("Read %d whitelist entries", $entries);
  $wtime = time();
}

sub InitSQLBlacklist {
  MailScanner::Log::InfoLog("Starting up SQL Blacklist");
  my $entries = CreateList('blacklist', \%Blacklist);
  MailScanner::Log::InfoLog("Read %d blacklist entries", $entries);
  $btime = time();
}

#
# Lookup a message in the by-domain whitelist and blacklist
#
sub SQLWhitelist {
  # Do we need to refresh the data?
  if ( (time() - $wtime) >= ($refresh_time * 60) ) {
   MailScanner::Log::InfoLog("Whitelist refresh time reached");
   InitSQLWhitelist();
  }
  my($message) = @_;
  return LookupList($message, \%Whitelist);
}

sub SQLBlacklist {
  # Do we need to refresh the data?
  if ( (time() - $btime) >= ($refresh_time * 60) ) {
   MailScanner::Log::InfoLog("Blacklist refresh time reached");
   InitSQLBlacklist();
  }
  my($message) = @_;
  return LookupList($message, \%Blacklist);
}


#
# Close down the by-domain whitelist and blacklist
#
sub EndSQLWhitelist {
  MailScanner::Log::InfoLog("Closing down by-domain spam whitelist");
}

sub EndSQLBlacklist {
  MailScanner::Log::InfoLog("Closing down by-domain spam blacklist");
}

sub CreateList {
  my($type, $BlackWhite) = @_;
  my($dbh, $sth, $sql, $to_address, $from_address, $count);
  my($db_name) = 'baruwa';
  my($db_host) = 'localhost';
  my($db_user) = 'root';
  my($db_pass) = '';
  
  # Connect to the database
  $dbh = DBI->connect("DBI:mysql:database=$db_name;host=$db_host",
                      $db_user, $db_pass,
                      {PrintError => 0}); 

  # Check if connection was successfull - if it isn't
  # then generate a warning and continue processing.
  if (!$dbh) {
   MailScanner::Log::WarnLog("Unable to initialise database connection: %s", $DBI::errstr);
   return;
  }

  $sql = "SELECT to_address, from_address FROM $type";
  $sth = $dbh->prepare($sql);
  $sth->execute;
  $sth->bind_columns(undef,\$to_address,\$from_address);
  $count = 0;
  while($sth->fetch()) {
   $BlackWhite->{lc($to_address)}{lc($from_address)} = 1; # Store entry
   $count++;
  }  

  # Close connections  
  $sth->finish();
  $dbh->disconnect();

  return $count;
}

#
# Based on the address it is going to, choose the right spam white/blacklist.
# Return 1 if the "from" address is white/blacklisted, 0 if not.
#
sub LookupList {
  my($message, $BlackWhite) = @_;

  return 0 unless $message; # Sanity check the input

  # Find the "from" address and the first "to" address
  my($from, $fromdomain, @todomain, $todomain, @to, $to, $ip);
  $from       = $message->{from};
  $fromdomain = $message->{fromdomain};
  @todomain   = @{$message->{todomain}};
  $todomain   = $todomain[0];
  @to         = @{$message->{to}};
  $to         = $to[0];
  $ip         = $message->{clientip};

  # It is in the list if either the exact address is listed,
  # or the domain is listed
  return 1 if $BlackWhite->{$to}{$from};
  return 1 if $BlackWhite->{$to}{$fromdomain};
  return 1 if $BlackWhite->{$to}{$ip};
  return 1 if $BlackWhite->{$to}{'default'};
  return 1 if $BlackWhite->{$todomain}{$from};
  return 1 if $BlackWhite->{$todomain}{$fromdomain};
  return 1 if $BlackWhite->{$todomain}{$ip};
  return 1 if $BlackWhite->{$todomain}{'default'};
  return 1 if $BlackWhite->{'default'}{$from};
  return 1 if $BlackWhite->{'default'}{$fromdomain};
  return 1 if $BlackWhite->{'default'}{$ip};

  # It is not in the list
  return 0;
}

1;
