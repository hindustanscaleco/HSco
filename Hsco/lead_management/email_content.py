def user(request,extra=''):
    if request.user.is_authenticated:
        name_mobile = str(request.user.name )+'''<br>
                        +91-'''+str( request.user.mobile )+'''<br>
                        <br>'''
    else:
        name_mobile = 'Team HSCo'+'''<br><br>'''
    text_content = ''' <html>
    <body>
              <p>'''+extra+'''</p>
               <br>
               <br>
               <p>
In case of any queries, please feel free to call us on the below numbers or visit our website at<a href="www.hindustanscale.com"> www.hindustanscale.com</a><br>
<br>
Thanks and Regards<br>
<br>
'''+name_mobile+'''
 

Hindustan Scale Company<br>

Sales Enquiry - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +91-7045922250<br>

Queries & Repairs - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+91-7045922251<br>

Feedback & Complaints - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+91-7045922252<br>

 <br>
 <a href="www.hindustanscale.com">
 <img  src="http://139.59.76.87/media/pi_history_file/hsco.jpg" style="width: 200px; height:100px;">
</a>

 <br>
 <br>

<span style="color: #ff6600;"> <b> An ISO 9001:2015 Certified Company  </b> </span> <br> <br>

 <img  src="http://139.59.76.87/media/pi_history_file/image002.jpg" style="width: 350px; height:120px;">
 <img  src="http://139.59.76.87/media/pi_history_file/image003.png" style="width: 180px; height:100px;"><br>

  <a href="https://play.google.com/store/apps/details?id=com.spryox.hsco&hl=en"> 	
  <img  src="http://139.59.76.87/media/pi_history_file/image004.png" style="width: 120px; height:100px;"></a>
</a>
 <img  src="http://139.59.76.87/media/pi_history_file/image005.png" style="width: 120px; height:100px;">
 <img  src="http://139.59.76.87/media/pi_history_file/image006.png" style="width: 120px; height:100px;">


</p>


         </body></html>'''
    return text_content

