% rebase('base.tpl')
スクリーン選択<br>
<form name="reportForm" method="post">
    <input type="checkbox" name="checkall" onClick="AllChecked();">全選択<br>
    {{ !report_form.screen }}<br>
    期間指定<br>
    {{ !report_form.time_from(value=last_month) }}
    ~
    {{ !report_form.time_till(value=this_month) }}<br>
    {{ !report_form.submit }}<br>
</from>

<script language="JavaScript" type="text/javascript">
    <!--
    function AllChecked(){
        var check = document.reportForm.checkall.checked;

        for (var i=0; i<document.reportForm.screen.length; i++){
            document.reportForm.screen[i].checked = check;
        }
    }
    //-->
</script>
