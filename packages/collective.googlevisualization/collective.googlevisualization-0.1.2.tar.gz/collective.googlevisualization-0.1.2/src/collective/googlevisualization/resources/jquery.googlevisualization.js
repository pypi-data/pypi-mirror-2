(function ($, google) {
    google.load('visualization', '1', {'packages': ['corechart', 
                                                'imagelinechart',
                                                'table',
                                                'imagesparkline']});


    $.gvisualization_defaults = {
        'ImageSparkLine' :  {width: 120, 
                            height: 40, 
                            labelPosition:'left',
                            showAxisLines: false,
                            showValueLabels: false},
        'BarChart' : {
            height: 600,
            width: 500,
            legend: 'bottom'
        },
        'ColumnChart': {
            height: 500,
            width: 700,
            legend: 'bottom'
        }
    };

    $.fn.gvisualization = function (options) {

        var el = $(this)[0];
        var self = $(this);

        var default_options = {
            type: 'BarChart',
            source: {
                url: null,
                dataType: 'json'
            },
            data: null,
            options: {}
        };

        options = $.extend(true, {}, default_options, options);

        var draw = function (data) {
            if (data.error) {
                self.empty();
                self.html(data.error);
                return
            };
            var table = new google.visualization.DataTable();
            $.each(data.columns, function (idx, column) {
                table.addColumn(column.type, column.label, column.id);
            });
            $.each(data.values, function (ridx, row) {
                table.addRows(1);
                $.each(row, function (cidx, cell) {
                    if (data.columns[cidx].type == 'date') {
                        table.setCell(ridx, cidx, new Date(cell));
                    } else {
                        table.setCell(ridx, cidx, cell);
                    };
                });
            });

            var plugin = google.visualization[options.type];
            var visualization = new plugin(el);

            var v_defaults = $.gvisualization_defaults[options.type] || {};
            visualization.draw(table, $.extend({}, v_defaults, options.options));
        };



        if (options.data) {
            draw(options.data);
        } else {
            options.source.success = draw;
            $.ajax(options.source);
        }
    };

})(jQuery, google);
