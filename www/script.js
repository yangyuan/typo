angular.module('typoApp', [])
    .controller('TypoController', ['$http', function ($http) {
        let typo = this;
        typo.swagger = {};
        typo.errors = [];
        typo.loading = false;
        typo.swagger_url = '';
        typo.share_url = '';


        typo.validateUrl = function () {
            $('#json-display').jsonViewer({}, []);
            typo.errors = [];
            typo.loading = true;
            typo.share_url = window.location.href.split('?')[0] + "?url=" + encodeURI(this.swagger_url);

            $http.post('/api/fetch',
                {url: this.swagger_url},
                {headers: {'Content-Type': 'application/json'}}
            ).then(
                function (response) {
                    typo.swagger = response.data;
                    $('#json-display').jsonViewer(typo.swagger, []);
                    typo.validateSwagger();
                },
                function (response) {
                    alert("Failed to load the swagger file from the URL.");
                    typo.loading = false;
                });

        };

        typo.validateFile = function () {
            $('#json-display').jsonViewer({}, []);
            typo.errors = [];
            typo.loading = true;
            typo.swagger_url = '';
            typo.share_url = '';

            let file = document.getElementById("swagger-file").files[0];
            if (file) {
                let reader = new FileReader();
                reader.readAsText(file, "UTF-8");
                reader.onload = function () {
                    let content = reader.result;
                    try {
                        typo.swagger = JSON.parse(content);
                        $('#json-display').jsonViewer(typo.swagger, []);
                        typo.validateSwagger();
                    } catch (e) {
                        alert("File doesn't contain validate swagger.");
                        typo.loading = false;
                    }
                };
                reader.onerror = function () {
                    alert('Failed to upload file.');
                    typo.loading = false;
                }
            } else {
                alert('No file selected.');
                typo.loading = false;
            }
        };

        typo.validateSwagger = function () {
            $http.post('/api/validate',
                this.swagger,
                {headers: {'Content-Type': 'application/json'}}
            ).then(
                function (response) {
                    typo.errors = response.data;
                    typo.loading = false;
                },
                function (response) {
                    alert('error validating swagger.');
                    typo.loading = false;
                });
        };

        typo.linkToError = function(error) {
            let link = error['path'].join('.');
            if (error['isKey']) {
                link = '$' + link;
            }
            return link;
        };

        typo.init = function () {
            let queries = {};

            try {
                $.each(document.location.search.substr(1).split('&'), function (c, q) {
                    let i = q.split('=');
                    queries[i[0].toString()] = i[1].toString();
                });
            } catch (e) {
                //
            }

            if (queries['url'] !== undefined) {

                typo.swagger_url = queries['url'];
                typo.validateUrl();
            }
        };

        typo.init();
    }]);