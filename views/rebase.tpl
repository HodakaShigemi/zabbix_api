% rebase('base.tpl')

<div class -"">

    <h1 class="page-header">ZabbixAPI</h1>

    <div class="form-group">

        % #describe host name element
        {{ !Form_host.hostname.label}}
        {{ !Form_host.hostname.(class_="form-control", placeholder=u"ホスト名を入力", maxlength = "50")}}

        % # print nature of error
        % if Form_host.hostname.errors:
            <div class="errors">
            % for error in Form_host.hostname.errors:
                <p class="text-danger">{{ error }}</p>
            % end
            </div>
        % end
    
    </div>

    <div class="form-group">

        % # describe element of item name
