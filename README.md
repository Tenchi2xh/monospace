<div align=right>
  <a href="https://pypi.org/project/monospace/"><img src="https://img.shields.io/pypi/v/monospace.svg?colorB=lightgrey" alt="PyPI" /></a>
  <a href="https://travis-ci.org/Tenchi2xh/monospace/"><img src="https://img.shields.io/travis/Tenchi2xh/monospace.svg" alt="Travis (.org)" /></a>
  <a href="https://www.codacy.com/app/Tenchi2xh/monospace"><img src="https://api.codacy.com/project/badge/Coverage/4c34d93852b246c0b2facdb93ff70fbe" alt="Coverage" /></a>
  <a href="https://www.codacy.com/app/Tenchi2xh/monospace"><img src="https://api.codacy.com/project/badge/Grade/4c34d93852b246c0b2facdb93ff70fbe" alt="Codacy grade" /></a>
</div>
<br/>

<pre>
                                                                                                             
                                                                                                             
                                                                                                             
                                                                                                             
                                                                                                             
                                                                                                             
                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━          
                             <a name="monospace"><b><i>Monospace</i></b></a>                                                                       
                                                                                                             
                                                                                                             
                                             ┌─────┬───┬───┬───┬───┬───┬───┬───┬───┐                         
                                             │ ╷ ╷ │ · │ ╷ │ · ├   ┤ · │ · │   ┤   ╡                         
                                             └─┴─┴─┴───┴─┴─┴───┴───┤ ┌─┴─┴─┴───┴───┘                         
                                                                   └─┘                                       
                                                  A fixed-width book typesetter                              
                                                                                                             
                             Contents:                                                                       
                                                                                                             
                             ⓪  <a href="#user-content-installation">ɪɴꜱᴛᴀʟʟᴀᴛɪᴏɴ</a>                                                                
                                                                                                             
                             ①  <a href="#user-content-usage">ᴜꜱᴀɢᴇ</a>                                                                       
                                                                                                             
                             ②  <a href="#user-content-markdown-format">ᴍᴀʀᴋᴅᴏᴡɴ ꜰᴏʀᴍᴀᴛ</a>                                                             
                                                                                                             
                                 ⓪  <a href="#user-content-settings">ꜱᴇᴛᴛɪɴɢꜱ</a>                                                                
                                                                                                             
                                 ①  <a href="#user-content-standard-markdown">ꜱᴛᴀɴᴅᴀʀᴅ ᴍᴀʀᴋᴅᴏᴡɴ</a>                                                       
                                                                                                             
                                 ②  <a href="#user-content-pandoc-features">ᴘᴀɴᴅᴏᴄ ꜰᴇᴀᴛᴜʀᴇꜱ</a>                                                         
                                                                                                             
                                 ③  <a href="#user-content-custom-elements">ᴄᴜꜱᴛᴏᴍ ᴇʟᴇᴍᴇɴᴛꜱ</a>                                                         
                                                                                                             
                             ③  <a href="#user-content-setting-up-a-development-environment">ꜱᴇᴛᴛɪɴɢ ᴜᴘ ᴀ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ</a>                                        
                                                                                                             
                                 ⓪  <a href="#user-content-poetry">ᴘᴏᴇᴛʀʏ</a>                                                                  
                                                                                                             
                                 ①  <a href="#user-content-git-hook">ɢɪᴛ ʜᴏᴏᴋ</a>                                                                
                                                                                                             
                                 ②  <a href="#user-content-sublime-text">ꜱᴜʙʟɪᴍᴇ ᴛᴇxᴛ</a>                                                            
                                                                                                             
                                 ③  <a href="#user-content-custom-repl">ᴄᴜꜱᴛᴏᴍ ʀᴇᴘʟ</a>                                                             
                                                                                                             
                                 ④  <a href="#user-content-building-the-fonts">ʙᴜɪʟᴅɪɴɢ ᴛʜᴇ ꜰᴏɴᴛꜱ</a>                                                      
                                                                                                             
                             TOWRITE: Intro                                                                  
                                                                                                             
     ━━━━━━━━━━━━━━━━━━━━                                                                                    
     <a name="installation"><b>Installation</b></a>            This project <i>requires</i> <a href="https://www.python.org/downloads/release/python-370/">ᴘʏᴛʜᴏɴ ₃.₇.₀</a> or later.                                    
                                                                                                             
     <i>Where the magic</i>         To install, run:                                                                
     <i>starts</i>                                                                                                  
                                 <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  <span style="color: #f8f8f2">pip</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">install</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">monospace</span>                                       </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
     ━━━━━━━━━━━━━━━━━━━━                                                                                    
     <a name="usage"><b>Usage</b></a>                   For now, Monospace only comes with one command, 𝚝𝚢𝚙𝚎𝚜𝚎𝚝:                        
                                                                                                             
     <i>RTFM</i>                        <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  Usage: monospace typeset [OPTIONS] MARKDOWN_FILE            </span>              
                                 <span style="background-color: #222222">                                                              </span>              
                                 <span style="background-color: #222222">    Typeset a markdown file into a book.                      </span>              
                                 <span style="background-color: #222222">                                                              </span>              
                                 <span style="background-color: #222222">    Saves the formatted book in the same directory as the     </span>              
                                 <span style="background-color: #222222">  input file.                                                 </span>              
                                 <span style="background-color: #222222">                                                              </span>              
                                 <span style="background-color: #222222">  Options:                                                    </span>              
                                 <span style="background-color: #222222">    -t, --to [ansi|html|ps|pdf]  Destination format.          </span>              
                                 <span style="background-color: #222222">  [required]                                                  </span>              
                                 <span style="background-color: #222222">    -p, --preview                Do not save a file,          </span>              
                                 <span style="background-color: #222222">                                 just print to stdout.        </span>              
                                 <span style="background-color: #222222">    -O, --open                   Open output file.            </span>              
                                 <span style="background-color: #222222">    -l, --linear                 Produce only one long page.  </span>              
                                 <span style="background-color: #222222">    --help                       Show this message and exit.  </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             Example usages:                                                                 
                                                                                                             
                             •   Typeset a file and preview the result in a terminal:                        
                                                                                                             
                                     <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                     <span style="background-color: #222222">  <span style="color: #f8f8f2">monospace</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">typeset</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">file.md</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">--to</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">ansi</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">--preview</span>           </span>              
                                     <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             •   Typeset a file into a contiguous html document, 𝚛𝚎𝚊𝚍𝚖𝚎.𝚑𝚝𝚖𝚕:                
                                                                                                             
                                     <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                     <span style="background-color: #222222">  <span style="color: #f8f8f2">monospace</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">typeset</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">README.md</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">--linear</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">--to</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">html</span>          </span>              
                                     <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             •   Typeset a file into a PDF book and open the result:                         
                                                                                                             
                                     <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                     <span style="background-color: #222222">  <span style="color: #f8f8f2">monospace</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">typeset</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">my_book.md</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">--to</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">pdf</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">--open</span>            </span>              
                                     <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
     ━━━━━━━━━━━━━━━━━━━━                                                                                    
     <a name="markdown-format"><b>Markdown format</b></a>         TOWRITE                                                                         
                                                                                                             
     <i>The nitty-gritty</i>        <a name="settings"><b>ꜱᴇᴛᴛɪɴɢꜱ</b></a>                                                                        
                                                                                                             
                             TOWRITE                                                                         
                                                                                                             
                             <a name="standard-markdown"><b>ꜱᴛᴀɴᴅᴀʀᴅ ᴍᴀʀᴋᴅᴏᴡɴ</b></a>                                                               
                                                                                                             
                             TOWRITE                                                                         
                                                                                                             
                             <a name="pandoc-features"><b>ᴘᴀɴᴅᴏᴄ ꜰᴇᴀᴛᴜʀᴇꜱ</b></a>                                                                 
                                                                                                             
                             TOWRITE                                                                         
                                                                                                             
                             <a name="custom-elements"><b>ᴄᴜꜱᴛᴏᴍ ᴇʟᴇᴍᴇɴᴛꜱ</b></a>                                                                 
                                                                                                             
                             TOWRITE                                                                         
                                                                                                             
     ━━━━━━━━━━━━━━━━━━━━                                                                                    
     <a name="setting-up-a-development-environment"><b>Setting up a devel-</b></a>     TOWRITE                                                                         
     <a name="XXX"><b>opment environment</b></a>                                                                                      
                             <a name="poetry"><b>ᴘᴏᴇᴛʀʏ</b></a>                                                                          
     <i>“So that they rhyme”</i>                                                                                    
     <i>— G. Lucas</i>              This project is managed and  packaged  by a promising  relatively  new          
                             tool, <a href="https://github.com/sdispater/poetry/">ᴘᴏᴇᴛʀʏ</a>. The package information and dependencies are declared in          
                             the 𝚙𝚢𝚙𝚛𝚘𝚓𝚎𝚌𝚝.𝚝𝚘𝚖𝚕 file, introduced in <a href="https://www.python.org/dev/peps/pep-0518/">ᴘᴇᴘ ₅₁₈</a>.                                 
                                                                                                             
                             To install Poetry, run:                                                         
                                                                                                             
                                 <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  <span style="color: #f8f8f2">pip</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">install</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">poetry</span>                                          </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             Poetry installs all  dependencies in an  isolated <a href="https://docs.python.org/3/tutorial/venv.html">ᴠɪʀᴛᴜᴀʟ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ</a>.          
                             By default, this virtual environment is  created  somewhere outside of          
                             the project directory, but it is more convenient to have it inside, so          
                             that IDEs like Sublime  Text  can  use  linters and type checkers from          
                             within the virtual environment:                                                 
                                                                                                             
                                 <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  <span style="color: #f8f8f2">poetry</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">settings.virtualenvs.in-project</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">true</span>                 </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             We can now install the project dependencies, including development de-          
                             pendencies:                                                                     
                                                                                                             
                                 <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  <span style="color: #f8f8f2">poetry</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">install</span>                                              </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             To run  commands in the  virtual environment,  it is possible  to  use          
                             𝚙𝚘𝚎𝚝𝚛𝚢 𝚛𝚞𝚗 or 𝚙𝚘𝚎𝚝𝚛𝚢 𝚜𝚑𝚎𝚕𝚕, however these are not very convenient. In-          
                             stead, we can <a href="https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments">ᴀᴄᴛɪᴠᴀᴛᴇ</a> it:                                                      
                                                                                                             
                                 <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  <span style="color: #f8f8f2">source</span><span style="color: #f8f8f2"> </span><span style="color: #f8f8f2">.venv/bin/activate</span>                                   </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             After activating, commands like 𝚙𝚒𝚙 and  𝚙𝚢𝚝𝚑𝚘𝚗  are all run with  the          
                             version specific to this  project, including dependencies. Development          
                             dependencies  also become  available, such  as the  commands  𝚙𝚢𝚝𝚎𝚜𝚝 ,          
                             𝚏𝚕𝚊𝚔𝚎𝟾 and 𝚖𝚢𝚙𝚢.                                                                
                                                                                                             
                             To avoid having to  remember how to activate  the virtual environment,          
                             here is useful alias to put in your bash configuration:                         
                                                                                                             
                                 <span style="background-color: #222222"><span style="color: #444444">▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔</span></span>              
                                 <span style="background-color: #222222">  alias pactivate='source $(poetry show -v | sed -n 1p | sed  </span>              
                                 <span style="background-color: #222222">   "s/^.*: \(.*\)$/\1/")/bin/activate'                        </span>              
                                 <span style="background-color: #222222"><span style="color: #444444">▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁</span></span>              
                                                                                                             
                             This will activate  the virtual  environment  for  the  current Poetry          
                             project (works also from a sub-directory inside that project).                  
                                                                                                             
                             <a name="git-hook"><b>ɢɪᴛ ʜᴏᴏᴋ</b></a>                                                                        
                                                                                                             
                             To ensure a standard of quality, the code  of this  project is checked          
                             with 𝚏𝚕𝚊𝚔𝚎𝟾 and 𝚖𝚢𝚙𝚢. They are part of the development dependencies in          
                             the project definition, and can be run inside the virtual environment.          
                                                                                                             
                             The script 𝚜𝚌𝚛𝚒𝚙𝚝𝚜/𝚌𝚑𝚎𝚌𝚔.𝚜𝚑 can  be  run to quickly check  everything,          
                             and a  <a href="https://githooks.com/">ɢɪᴛ ʜᴏᴏᴋ</a> is provided at 𝚜𝚌𝚛𝚒𝚙𝚝𝚜/𝚙𝚛𝚎-𝚌𝚘𝚖𝚖𝚒𝚝. To enable the hook,          
                             just copy the file to .𝚐𝚒𝚝/𝚑𝚘𝚘𝚔𝚜. The check  will  happen  before each          
                             commit.                                                                         
                                                                                                             
                             <a name="sublime-text"><b>ꜱᴜʙʟɪᴍᴇ ᴛᴇxᴛ</b></a>                                                                    
                                                                                                             
                             A .𝚜𝚞𝚋𝚕𝚒𝚖𝚎-𝚙𝚛𝚘𝚓𝚎𝚌𝚝 file is provided to set up things around in <a href="https://www.sublimetext.com/">ꜱᴜʙʟɪᴍᴇ</a>          
                             <a href="XXX">ᴛᴇxᴛ</a>:                                                                           
                                                                                                             
                             •   Configuration     for     <a href="https://github.com/SublimeLinter/SublimeLinter">ꜱᴜʙʟɪᴍᴇʟɪɴᴛᴇʀ    </a>:    if     you    have          
                                 <a href="https://github.com/fredcallaway/SublimeLinter-contrib-mypy">ꜱᴜʙʟɪᴍᴇʟɪɴᴛᴇʀ-ᴄᴏɴᴛʀɪʙ-ᴍʏᴘʏ</a> and <a href="https://github.com/SublimeLinter/SublimeLinter-flake8">ꜱᴜʙʟɪᴍᴇʟɪɴᴛᴇʀ-ꜰʟᴀᴋᴇ₈ </a> installed, it          
                                 will configure them to point to the virtual environment’s executa-          
                                 bles.                                                                       
                                                                                                             
                             •   A  few  ignored  folders  to  hide  some  things  covered  in  the          
                                 .𝚐𝚒𝚝𝚒𝚐𝚗𝚘𝚛𝚎 file.                                                            
                                                                                                             
                             <a name="custom-repl"><b>ᴄᴜꜱᴛᴏᴍ ʀᴇᴘʟ</b></a>                                                                     
                                                                                                             
                             TOWRITE                                                                         
                                                                                                             
                             <a name="building-the-fonts"><b>ʙᴜɪʟᴅɪɴɢ ᴛʜᴇ ꜰᴏɴᴛꜱ</b></a>                                                              
                                                                                                             
                             TOWRITE                                                                         
                                                                                                             
                                                                                                             
                                                                                                             
                                                                                                             
                                                                                                             
</pre>
