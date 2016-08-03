<html>

% include('header.tpl')

<body>
<div class="container">
    <header>
        <h1 class="page-deader">{{title}}</h1>
    </header>

    <nav>
        <ul>
        % if request.path == '/top':
            <li class="active"><a href="./top">Top画面</a></li>
        % else:
            <li><a href="./top">Top画面</a></li>
        %end

        % if request.path == '/history':
            <li class="active"><a href="./history">取得値の一覧取得</a></li>
        % else:
            <li><a href="./history">取得値の一覧取得</a></li>
        %end

        % if request.path == '/report':
            <li class="active"><a href="./report">受光レポート取得</a></li>
        % else:
            <li><a href="./report">受光レベルレポート取得</a></li>
        %end
        </ul>
    </nav>

    <article>

        {{!base}}

    </article>

    <footer>操作不明点、バグ等の報告は重見まで</footer>
</div>
</body>
</html>
