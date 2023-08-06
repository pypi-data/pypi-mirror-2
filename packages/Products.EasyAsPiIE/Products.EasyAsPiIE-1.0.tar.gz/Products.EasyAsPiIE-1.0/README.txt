Introduction
============
This product allows you to make sites faster since you don't need to worry about some of the hang ups from Internet Explorer. 

1.) Just by installing this product you don't have to worry about transparent PNG's in IE 6. 

2.) New features include being able to do CSS 3 (Uses css3pie http://css3pie.com/) type things in IE 6,7,8. Things like border-radius, box-shadow, text-shadow.

A.) To use the CSS 3 features make a ie only css file and add your file into the css area of main_template. In Plone 4 you can just add the condition for the css registry file.
        <!--[if lt IE 9]><link href="IEFixes_foo.css"  media="screen" type="text/css" rel="stylesheet"> <![endif]-->
        
B.) Add these 2 lines to your css class or id.
behavior: url(&dtml-portal_url;/PIE.htc);
position: relative;

Make a list of classes that need to be changed in IE in your IEFixes_foo.css file. Example:
#portal-personaltools,
.portalHeader,
.fooclass {
 behavior: url(&dtml-portal_url;/PIE.htc); 
    position: relative; 
    }

C.)  Issues with CSSPie.. You can't do less then all four border-radius easily:
.portalHeader {
border-top-left-radius: 10px;
border-bottom-left-radius: 10px;
}

should be:

.portalHeader {
    border-radius: 10px 0px 0px 10px;
}


Also, if you are are doing gradients there is a hook:

#portal-header {
    -pie-background: linear-gradient(#D3D4D5, #FEFEFE); /*PIE*/ 
}


*Version 0.91 Fix 
The 0.81 product was showing up twice and causing problems.  

The fix is to take the old version out of your buildout. 

Then rerun buildout. 

Next go into your ZMI and go to the control panel. Make sure anything that says EasyAsPiIE is deleted. Restart zope and recheck.

Now get the upgrade in your buildout. 

You should be set.

The reason this broke is that this is a problem with paster. Anything with "Products.**" can't have the one line of code in the config.py starting with <registers.***

https://weblion.psu.edu/trac/weblion/wiki/PloneTroubleshooting