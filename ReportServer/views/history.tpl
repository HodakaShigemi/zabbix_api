% rebase('base.tpl')

<form method="post">
<select id ="host_id" name="host_id" onChange="this.form.submit()">
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
    <form method="post">
        {{ !item_history_form.item }}<br>
        {{ !item_history_form.description }}<br>
        {{ !item_history_form.time_from(value=last_month) }}
        ~
        {{ !item_history_form.time_till(value=this_month) }}
        {{ !item_history_form.submit }}
    </form>
% except TypeError:
% pass
% end
