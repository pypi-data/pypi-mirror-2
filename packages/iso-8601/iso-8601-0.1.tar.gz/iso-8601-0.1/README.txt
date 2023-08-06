iso-8601
===========

Correctly parse a valid ISO 8601 datetime string.

At this stage, only datetime (or non-truncated date) formats are permitted.

Week number formats are not permitted in this version.

You can have an object in any of the following formats:

	* YYYY-MM-DD
	* YYYYMMDD
	* YYYY-MM-DDThh
	* YYYYMMDDThh
	* YYYY-MM-DDThh:mm
	* YYYYMMDDThhmm
	* YYYY-MM-DDThh:mm:ss
	* YYYYMMDDThhmmss

Additionally, to support some legacy systems, in all cases the T can be
replaced by a space. Essentially, this just combines the two representations,
which is not strictly according to the specification, but is commonly used.

Also supported is using an hour of 24 to mean midnight at the end of the
day: this is converted to the python object of the next day's 00:00:00.

Finally, only naive datetime objects are supported at this time. Timezones
may not be included in the format string.

Future (in no particular order):

	* Support timezones
	* Support durations
	* Support time intervals
	* Support repeating intervals
	* Support week-dates
	* Support truncated dates
	* Support times (including truncated?)

The following references were used to determine supported formats:

	* http://en.wikipedia.org/wiki/ISO_8601
	* http://dotat.at/tmp/ISO_8601-2004_E.pdf

