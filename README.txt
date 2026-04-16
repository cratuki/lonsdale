Lonsdale Markup Language


// Project goal

Create a domain-specific language for the following,

    Modeling the design of vehicles

    Construction/modification steps for vehicles


// Quick introuduction

You can see designs for vehicles in the /design folder of this project.

xxx Add a link to a running version of the browser app.

Lonsdale is build on a markup system /Interface Script/. If you know what XML
is - it is similar to this, but easier to work with when humans are making
edits. https://github.com/cratuki/interface_script_py


// Get a github account

Before you get started, create a user account on github.com. This will allow
you to send questions to me if you get stuck.


// Review open Issues

The github system has a concept called /Issues/. Each Issue is a public forum.

Here are the issues for this project:
https://github.com/cratuki/lonsdale/issues?q=is%3Aissue


// How to ask a question or make a suggestion

Here I will describe how to send me a public message that is called an Issue.

Important. The text of Issues is public. Do not put confidential information
like phone numbers or passwords in the text you write here.

Follow these steps to raise an Issue to me,

    In your web browser, go to https://github.com/cratuki/lonsdale/issues/new

    Type in a subject and text.

    Click the green "create" button.

In time I will review your email and either give you a personalised response,
or point you to existing discussion related to your matter.

Important. This is not an email, it is a public message. Do not put sensitive
information in the text.


// Windows users, non-programmers

This section describes steps you would take to get the Lonsdale system running
if you use Windows.

To run this tool, you need at least the following,

    Windows 10 or better.

    To have the python3 programming environment installed, at least version
    3.8. You can get python from here:
    https://www.python.org/ftp/python/3.13.13/python-3.13.13-amd64.exe

Steps,

    Download the project as follows,

        Be on this web page: https://github.com/cratuki/lonsdale
        (You probably are already)

        Click on the green github button [Code], then select [Download zip]. That
        will download a zip file of the system.

    Find the zip file in your downloads area. Right click on it, and select an
    option to expand it to your disk. You want it expanded do c:\lml.

    Open a Command Prompt by pressing the windows key, typing "cmd" and then
    selecting the black box icon.

    Within the command prompt, type these commands,

        c:
        cd c:\lml
        build.bat
            # This will compiler the markup language.

    If you want to modify the markup language yourself,

        Open a text editor. Windows comes with a free one called Notepad.

        Open the file you want to change from c:\lml\design

        Save your changes.

        Run the steps in the command prompt, as described above.

        If it complains, pay attention to the text. It tries to give good
        hints about why it is unhappy.


// Windows users, programmers

Requirements: windows 10 or greater, python3, git client.

Clone the repository to your system.

From a command prompt, run build.bat.

The files for you to edit are in design.


// Linux and Mac users, assumes you are comfortable with the terminal

Requirements: git client, python3.

Clone the repository to your system.

python3 -B -m src.app_lonsdale
    # Or look in the script ./app - I generally use this as my launcher, and
    # edit it as I am working.

The files for you to edit are in design.


// Q&A

... Why not compose cars as recipes?

Let's just cover the essence of this idea with an example,

    There would be a recipe that let you take a gearbox and a torque tube and
    a diff, and which would output a drive-train.

    Then there would be a recipe that would take a drive-train and some wheels
    and a front suspension and a rear-suspension and an interior and an
    engine, and that would output a vehicle.

    In this way, by the end of the construction notation, you would have a
    single remaining node, which would be the finished vehicle.

I call this a /craft-centric/ approach. I played with this approach during the
design of the system, and decided it would be a poor path forward.

Distraction of having to identify intermediate states.

    You would need to spend mental energy deciding what was and was not in the
    different composition parts. For example, are the trailing arms part of
    the drive train? What about the brake system? What about the brake pads?

    You would need to come up with distinct and unique names for all of these
    composable things.

    This creates a type of work that is not an inherent complexity to the goal
    of designing a car.

    The designer's mind would easily get lost in the sea of crafting
    transitions, it would feel like hard work, and it would get annoying
    because it should not matter.

Lonsdale as it is designed places a lot of emphasis on the connections between
things. That is inherent complexity.

Imagine if there was a 5v wire within the car and a 12v wire. How would you
ensure that the design was not running 12V into 5V circuits?

The connection syntax of the current syntax accounts for this. Whereas I think
craft-centric would struggle to accomodate this.


// Prompt for review work with AI instances

Lonsdale Markup is a Domain-Specific Language (DSL) designed for the
high-level management and structural validation of complex engineering
projects. It builds on conventions established by Interface Script
(http://songseed.org/post/20200607.aa.interface_script.html).

The project bridges the gap between conceptual engineering and remote project
management by enforcing physical and logical "contracts" between components.

The notation prioritizes the logic of connectivity, and not CAD geometry. The
immediate focus is restoration of a peugeot 504.

Qualities of the system,

    Connection-Centric: The system focuses on how parts mate. It defines
    "Connection Standards" (CS) to ensure that interfaces (like a gearbox
    bellhousing or a torque tube ball) are physically and logically
    compatible.

    Ledger-Based Status: By tracking "Nodes" (real physical objects) across
    different "Sites" (workshops, storage, benches), the DSL maintains an
    audit trail of where parts are and what state they are in.

    Gap Analysis (The "Killer Feature"): The compiler compares a "Design Site"
    (the perfect car) against a "Physical Site" (the car in the shop). It
    identifies missing links, incompatible parts, or incomplete "Recipes"
    (assembly instructions).

Technical Implementation

    Compiler: A Python-based tool that consumes the Lonsdale Markup, validates
    the graph of connections, and generates reports.

    License: MIT-licensed, intended as a sturdy, human-readable "settlement"
    for engineers to reclaim structural clarity from complex, poorly
    documented systems.









