
-------------------------------------------------------------------------------
Stack
-------------------------------------------------------------------------------
Requirements

o  Has to be web app from the get go to make it easy for people to engage with
o  Has to be simple and familiar - cannot spend time on this
o  Need persistence
o  Nice if could very simple deploy using docker or app engine
o  Will need to move to enterprise IT eventually

Implications

o  Has to be Python
o  Can be trad server side html templating
o  Rule out server based DB
o  Rule out GAE
o  Can use Flask-Shelve for persistence.

Conclusions

o  Flask should be baseline
o  Find trivial file based key value store (value is entire db in yaml, or
   json)

-------------------------------------------------------------------------------
Deployment
-------------------------------------------------------------------------------
Docker image comprising Flask, Shelve, and Bootstrap with GUnicorn or CherryPy
as WSGI server.
Using mounted volume to allow dev iteration.
Deployed eventually on DNAe server, but in mean time, GCE or EC2 instance, and
even sooner locally.
