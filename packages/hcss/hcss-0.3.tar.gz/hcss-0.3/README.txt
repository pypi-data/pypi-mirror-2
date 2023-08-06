hcss is a CSS compiler that that allows you to use HTML element hierarchy to define CSS rules. hcss employs simple conventions for defining nested rules and minimalist class inheritance. Requires Python 2.2+. If easy_install is already available, just use that, otherwise, install pip[1]. BSD-licensed.

Input:

    <div id="parent">
      margin: 10px;
      <div class="child">
        margin: 5px;
        border: 1px solid #000;
      </div>
    </div>
    
Output:

    div#parent {
      margin: 10px;
    }
    div#parent > div.child {
      margin: 5px;
      border: 1px solid #000;
    }
    
    
Please refer to 

  http://jonasgalvez.com.br/Software/HCSS.html 
  
for further info.

Pull requests are welcome.

[1] http://pip.openplans.org/