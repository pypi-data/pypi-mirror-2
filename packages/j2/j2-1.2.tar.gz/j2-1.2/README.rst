OVERVIEW
--------

j2 is commandline text templating & rendering tool, it brings the power of the Jinja2 engine to general
purpose text compilation. The tool excels at the various situations where you need to compile/generate
text files as part of a build system or other types of automation process (sysadmin to configuration
files etc)


DESCRIPTION
-----------

Jinja2 is a very capable templating system used throughout the Python community. Its features &
capabilities are extensive & robust. However to access, one typically writes a python application or
script and programatically loads & renders templates.

j2 makes this Jinja2 templating available on the command line. Using an MVC metaphor, think of the python
file foo.py (module foo) as the (M)odel, a template file template.j2t as the (View) and the commandline
j2 interface as the (C)ontroller.

Template files (usually suffixed with j2t) are simply normal Jinja2 templates. The format of these files
is extensively documented at the Jinja2 project homepage.

Modules are just a fancy word for py files. They provide the mechanism to load the context that is used
in rendering the template. All modules are loaded into the global namespace via an exec of "from module
import \*". The entire global namespace is then made available in the templates for rendering.

The combination of templates and flexible module loading makes j2 a very useful tool in code generation
or any other general purpose cmdline template processing. We have been using j2 successfully in our build
environment similarly to a compiler for rendering templates into output files.


OUR PROBLEM & SOLUTION
----------------------

J2 was developed after I saw yet another hideously borked mechanism that someone hacked together to
generate text files as part of our build system. I just couldnt take it anymore and knew there were
simpler, robust & featureful mechanisms to handle text processing.

Being a lazy hacker (I come from Perl community. ;-) I considered using one of the many existing tools.
And make no mistake, there are a lot of existing text processing utilities that could be used or abused
to achieve the goal. Some examples are cpp, m4, sed/awk, bash, DOS batfiles (We need to support Windows),
perl, python, etc. Unfortunately each had significant issues, too ugly (m4, sed/awk, DOS), too limited
(cpp), poor coupling (bash, perl, python, ruby).

Since I had experience using Sphinx for some documentation and I really liked the Jinja2 templating
system I decided to put a cmdline frontend on Jinja2 and use a familiar MVC model to separate the logic
in the models and the templates.

After the first prototype of j2 was shown to some engineers internally it use spread like wild fire
very quickly thoughout our build systems. Engineers were ripping out old complicated & brittle tools
(aka hacks) and replacing them with j2. We found our models could extract key metadata regarding our
product features from Excel, from xml, from basically anything and then very easily create templates to
autogenerate files.

J2's use even spread beyond its original intent of use in our build system. One engineer after seeing
j2, leveraged an existing model file that had access to some per product features, and used it to
autogenerate a battery of component tests tailored specifically to each product.

Net net, its been a big help in our system. We have replaced numerous old mechanisms for generating text
files, this has resuluted in deleting thousands of lines of code from a mish mash of languages (DOS
bat files all the way to C++ code) encouraging more reuse & sharing (via models) and standardized our
approach. This is making it much easier to develop, debug & maintain a large complex build system.


MORE INFO
-----------
In the source tree see doc/info.txt for a detailed man page with multiple usage examples.
