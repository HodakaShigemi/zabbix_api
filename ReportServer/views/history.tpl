% rebase('base.tpl')

ホスト選択<br>
<form method="post">
<select id ="host_name" name="host_name" onChange="this.form.submit()">
% for host_name in host_names:
    % if selected_host == host_name:
        <option value="{{ host_name }}" selected>{{ host_name }}</option>
    % else:
        <option value="{{ host_name }}">{{ host_name }}</option>
    % end
% end
</select>
</form>

% try:
アイテム・時間指定<br>
<form method='post'>
    {{ !item_history_form.item }}<br>
    {{ !item_history_form.time_from(value=last_month) }}
    ~
    {{ !item_history_form.time_till(value=this_month) }}
    {{ !item_history_form.submit }}
</form>
% except TypeError:
% pass
% end
