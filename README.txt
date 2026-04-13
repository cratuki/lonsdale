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

I call this a /craft-centric/ approach.

I expect this would work for toy examples, but would scale up poorly.

Work put into this is not concerned with the problems that the designer should
want to be spending their energy on.

Distraction of having to identify intermediate states.

    You would need to spend mental energy deciding what was and was not in the
    different composition parts. For example, are the trailing arms part of
    the drive train? What about the brake system? What about the brake pads?

    You would need to come up with distinct and unique names for all of these
    composable things.

    The designer's mind would easily get lost in the sea of crafting
    transitions, it would feel like hard work, beyond a certain point it would
    feel like complexity soup.

    Separately, it is not clear how this model would emphasise the connections
    between things. Imagine if there was a 5v line within the car and a 12v
    car. The connection syntax of the current syntax accounts for this. It is
    not clear to me how this everything-is-crafted 

    Veteran programmers are often wary of a dynamic in object-oriented
    programming that emerges from implementation inheritance. I feel similar
    kinds of problems coming through in this model.

The Lonsdale system as it is designed places a lot of emphasis on connections
between things. This is valuable. I think this would be lost if I had instead
pursued the craft-centric approach.






