<html>
<header>
</header>
<body>
{{ !form.host_id.label}}
<form method='post'>
        {{ !form.host_id(onChange='this.form.submit()')}}
</form>
    % try:
        {{ host_info}}
    <% except NameError:
    pass
    end %>
    % try:
<form method='post'>
        {{ !form.items_id}}
        {{ !form.from_time}}
        {{ !form.to_time}}
        {{ !form.save}}
</form>
    <% except TypeError:
    pass
    end %>
</body>
</html>
