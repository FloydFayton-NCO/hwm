/*
 Highcharts JS v4.1.1 (2015-02-17)

 (c) 2009-2014 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(k, D) {
    function K(a, b, c) {
        this.init.call(this, a, b, c)
    }
    var P = k.arrayMin
      , Q = k.arrayMax
      , u = k.each
      , H = k.extend
      , o = k.merge
      , R = k.map
      , q = k.pick
      , x = k.pInt
      , p = k.getOptions().plotOptions
      , g = k.seriesTypes
      , v = k.extendClass
      , L = k.splat
      , r = k.wrap
      , M = k.Axis
      , y = k.Tick
      , I = k.Point
      , S = k.Pointer
      , T = k.CenteredSeriesMixin
      , z = k.TrackerMixin
      , s = k.Series
      , w = Math
      , E = w.round
      , B = w.floor
      , N = w.max
      , U = k.Color
      , t = function() {};
    H(K.prototype, {
        init: function(a, b, c) {
            var d = this
              , e = d.defaultOptions;
            d.chart = b;
            if (b.angular)
                e.background = {};
            d.options = a = o(e, a);
            (a = a.background) && u([].concat(L(a)).reverse(), function(a) {
                var h = a.backgroundColor
                  , b = c.userOptions
                  , a = o(d.defaultBackgroundOptions, a);
                if (h)
                    a.backgroundColor = h;
                a.color = a.backgroundColor;
                c.options.plotBands.unshift(a);
                b.plotBands = b.plotBands || [];
                b.plotBands.unshift(a)
            })
        },
        defaultOptions: {
            center: ["50%", "50%"],
            size: "85%",
            startAngle: 0
        },
        defaultBackgroundOptions: {
            shape: "circle",
            borderWidth: 1,
            borderColor: "silver",
            backgroundColor: {
                linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 0,
                    y2: 1
                },
                stops: [[0, "#FFF"], [1, "#DDD"]]
            },
            from: -Number.MAX_VALUE,
            innerRadius: 0,
            to: Number.MAX_VALUE,
            outerRadius: "105%"
        }
    });
    var G = M.prototype
      , y = y.prototype
      , V = {
        getOffset: t,
        redraw: function() {
            this.isDirty = !1
        },
        render: function() {
            this.isDirty = !1
        },
        setScale: t,
        setCategories: t,
        setTitle: t
    }
      , O = {
        isRadial: !0,
        defaultRadialGaugeOptions: {
            labels: {
                align: "center",
                x: 0,
                y: null
            },
            minorGridLineWidth: 0,
            minorTickInterval: "auto",
            minorTickLength: 10,
            minorTickPosition: "inside",
            minorTickWidth: 1,
            tickLength: 10,
            tickPosition: "inside",
            tickWidth: 2,
            title: {
                rotation: 0
            },
            zIndex: 2
        },
        defaultRadialXOptions: {
            gridLineWidth: 1,
            labels: {
                align: null,
                distance: 15,
                x: 0,
                y: null
            },
            maxPadding: 0,
            minPadding: 0,
            showLastLabel: !1,
            tickLength: 0
        },
        defaultRadialYOptions: {
            gridLineInterpolation: "circle",
            labels: {
                align: "right",
                x: -3,
                y: -2
            },
            showLastLabel: !1,
            title: {
                x: 4,
                text: null,
                rotation: 90
            }
        },
        setOptions: function(a) {
            a = this.options = o(this.defaultOptions, this.defaultRadialOptions, a);
            if (!a.plotBands)
                a.plotBands = []
        },
        getOffset: function() {
            G.getOffset.call(this);
            this.chart.axisOffset[this.side] = 0;
            this.center = this.pane.center = T.getCenter.call(this.pane)
        },
        getLinePath: function(a, b) {
            var c = this.center
              , b = q(b, c[2] / 2 - this.offset);
            return this.chart.renderer.symbols.arc(this.left + c[0], this.top + c[1], b, b, {
                start: this.startAngleRad,
                end: this.endAngleRad,
                open: !0,
                innerR: 0
            })
        },
        setAxisTranslation: function() {
            G.setAxisTranslation.call(this);
            if (this.center)
                this.transA = this.isCircular ? (this.endAngleRad - this.startAngleRad) / (this.max - this.min || 1) : this.center[2] / 2 / (this.max - this.min || 1),
                this.minPixelPadding = this.isXAxis ? this.transA * this.minPointOffset : 0
        },
        beforeSetTickPositions: function() {
            this.autoConnect && (this.max += this.categories && 1 || this.pointRange || this.closestPointRange || 0)
        },
        setAxisSize: function() {
            G.setAxisSize.call(this);
            if (this.isRadial) {
                this.center = this.pane.center = k.CenteredSeriesMixin.getCenter.call(this.pane);
                if (this.isCircular)
                    this.sector = this.endAngleRad - this.startAngleRad;
                this.len = this.width = this.height = this.center[2] * q(this.sector, 1) / 2
            }
        },
        getPosition: function(a, b) {
            return this.postTranslate(this.isCircular ? this.translate(a) : 0, q(this.isCircular ? b : this.translate(a), this.center[2] / 2) - this.offset)
        },
        postTranslate: function(a, b) {
            var c = this.chart
              , d = this.center
              , a = this.startAngleRad + a;
            return {
                x: c.plotLeft + d[0] + Math.cos(a) * b,
                y: c.plotTop + d[1] + Math.sin(a) * b
            }
        },
        getPlotBandPath: function(a, b, c) {
            var d = this.center, e = this.startAngleRad, f = d[2] / 2, h = [q(c.outerRadius, "100%"), c.innerRadius, q(c.thickness, 10)], i = /%$/, m, l = this.isCircular;
            this.options.gridLineInterpolation === "polygon" ? d = this.getPlotLinePath(a).concat(this.getPlotLinePath(b, !0)) : (a = Math.max(a, this.min),
            b = Math.min(b, this.max),
            l || (h[0] = this.translate(a),
            h[1] = this.translate(b)),
            h = R(h, function(a) {
                i.test(a) && (a = x(a, 10) * f / 100);
                return a
            }),
            c.shape === "circle" || !l ? (a = -Math.PI / 2,
            b = Math.PI * 1.5,
            m = !0) : (a = e + this.translate(a),
            b = e + this.translate(b)),
            d = this.chart.renderer.symbols.arc(this.left + d[0], this.top + d[1], h[0], h[0], {
                start: Math.min(a, b),
                end: Math.max(a, b),
                innerR: q(h[1], h[0] - h[2]),
                open: m
            }));
            return d
        },
        getPlotLinePath: function(a, b) {
            var c = this, d = c.center, e = c.chart, f = c.getPosition(a), h, i, m;
            c.isCircular ? m = ["M", d[0] + e.plotLeft, d[1] + e.plotTop, "L", f.x, f.y] : c.options.gridLineInterpolation === "circle" ? (a = c.translate(a)) && (m = c.getLinePath(0, a)) : (u(e.xAxis, function(a) {
                a.pane === c.pane && (h = a)
            }),
            m = [],
            a = c.translate(a),
            d = h.tickPositions,
            h.autoConnect && (d = d.concat([d[0]])),
            b && (d = [].concat(d).reverse()),
            u(d, function(f, c) {
                i = h.getPosition(f, a);
                m.push(c ? "L" : "M", i.x, i.y)
            }));
            return m
        },
        getTitlePosition: function() {
            var a = this.center
              , b = this.chart
              , c = this.options.title;
            return {
                x: b.plotLeft + a[0] + (c.x || 0),
                y: b.plotTop + a[1] - {
                    high: 0.5,
                    middle: 0.25,
                    low: 0
                }[c.align] * a[2] + (c.y || 0)
            }
        }
    };
    r(G, "init", function(a, b, c) {
        var j;
        var d = b.angular, e = b.polar, f = c.isX, h = d && f, i, m;
        m = b.options;
        var l = c.pane || 0;
        if (d) {
            if (H(this, h ? V : O),
            i = !f)
                this.defaultRadialOptions = this.defaultRadialGaugeOptions
        } else if (e)
            H(this, O),
            this.defaultRadialOptions = (i = f) ? this.defaultRadialXOptions : o(this.defaultYAxisOptions, this.defaultRadialYOptions);
        a.call(this, b, c);
        if (!h && (d || e)) {
            a = this.options;
            if (!b.panes)
                b.panes = [];
            this.pane = (j = b.panes[l] = b.panes[l] || new K(L(m.pane)[l],b,this),
            l = j);
            l = l.options;
            b.inverted = !1;
            m.chart.zoomType = null;
            this.startAngleRad = b = (l.startAngle - 90) * Math.PI / 180;
            this.endAngleRad = m = (q(l.endAngle, l.startAngle + 360) - 90) * Math.PI / 180;
            this.offset = a.offset || 0;
            if ((this.isCircular = i) && c.max === D && m - b === 2 * Math.PI)
                this.autoConnect = !0
        }
    });
    r(y, "getPosition", function(a, b, c, d, e) {
        var f = this.axis;
        return f.getPosition ? f.getPosition(c) : a.call(this, b, c, d, e)
    });
    r(y, "getLabelPosition", function(a, b, c, d, e, f, h, i, m) {
        var l = this.axis
          , j = f.y
          , n = 20
          , g = f.align
          , A = (l.translate(this.pos) + l.startAngleRad + Math.PI / 2) / Math.PI * 180 % 360;
        l.isRadial ? (a = l.getPosition(this.pos, l.center[2] / 2 + q(f.distance, -25)),
        f.rotation === "auto" ? d.attr({
            rotation: A
        }) : j === null && (j = l.chart.renderer.fontMetrics(d.styles.fontSize).b - d.getBBox().height / 2),
        g === null && (l.isCircular ? (this.label.getBBox().width > l.len * l.tickInterval / (l.max - l.min) && (n = 0),
        g = A > n && A < 180 - n ? "left" : A > 180 + n && A < 360 - n ? "right" : "center") : g = "center",
        d.attr({
            align: g
        })),
        a.x += f.x,
        a.y += j) : a = a.call(this, b, c, d, e, f, h, i, m);
        return a
    });
    r(y, "getMarkPath", function(a, b, c, d, e, f, h) {
        var i = this.axis;
        i.isRadial ? (a = i.getPosition(this.pos, i.center[2] / 2 + d),
        b = ["M", b, c, "L", a.x, a.y]) : b = a.call(this, b, c, d, e, f, h);
        return b
    });
    p.arearange = o(p.area, {
        lineWidth: 1,
        marker: null,
        threshold: null,
        tooltip: {
            pointFormat: '<span style="color:{series.color}">●</span> {series.name}: <b>{point.low}</b> - <b>{point.high}</b><br/>'
        },
        trackByArea: !0,
        dataLabels: {
            align: null,
            verticalAlign: null,
            xLow: 0,
            xHigh: 0,
            yLow: 0,
            yHigh: 0
        },
        states: {
            hover: {
                halo: !1
            }
        }
    });
    g.arearange = v(g.area, {
        type: "arearange",
        pointArrayMap: ["low", "high"],
        toYData: function(a) {
            return [a.low, a.high]
        },
        pointValKey: "low",
        deferTranslatePolar: !0,
        highToXY: function(a) {
            var b = this.chart
              , c = this.xAxis.postTranslate(a.rectPlotX, this.yAxis.len - a.plotHigh);
            a.plotHighX = c.x - b.plotLeft;
            a.plotHigh = c.y - b.plotTop
        },
        getSegments: function() {
            var a = this;
            u(a.points, function(b) {
                if (!a.options.connectNulls && (b.low === null || b.high === null))
                    b.y = null;
                else if (b.low === null && b.high !== null)
                    b.y = b.high
            });
            s.prototype.getSegments.call(this)
        },
        translate: function() {
            var a = this
              , b = a.yAxis;
            g.area.prototype.translate.apply(a);
            u(a.points, function(a) {
                var d = a.low
                  , e = a.high
                  , f = a.plotY;
                e === null && d === null ? a.y = null : d === null ? (a.plotLow = a.plotY = null,
                a.plotHigh = b.translate(e, 0, 1, 0, 1)) : e === null ? (a.plotLow = f,
                a.plotHigh = null) : (a.plotLow = f,
                a.plotHigh = b.translate(e, 0, 1, 0, 1))
            });
            this.chart.polar && u(this.points, function(c) {
                a.highToXY(c)
            })
        },
        getSegmentPath: function(a) {
            var b, c = [], d = a.length, e = s.prototype.getSegmentPath, f, h;
            h = this.options;
            var i = h.step;
            for (b = HighchartsAdapter.grep(a, function(a) {
                return a.plotLow !== null
            }); d--; )
                f = a[d],
                f.plotHigh !== null && c.push({
                    plotX: f.plotHighX || f.plotX,
                    plotY: f.plotHigh
                });
            a = e.call(this, b);
            if (i)
                i === !0 && (i = "left"),
                h.step = {
                    left: "right",
                    center: "center",
                    right: "left"
                }[i];
            c = e.call(this, c);
            h.step = i;
            h = [].concat(a, c);
            this.chart.polar || (c[0] = "L");
            this.areaPath = this.areaPath.concat(a, c);
            return h
        },
        drawDataLabels: function() {
            var a = this.data, b = a.length, c, d = [], e = s.prototype, f = this.options.dataLabels, h = f.align, i, m = this.chart.inverted;
            if (f.enabled || this._hasPointLabels) {
                for (c = b; c--; )
                    if (i = a[c],
                    i.y = i.high,
                    i._plotY = i.plotY,
                    i.plotY = i.plotHigh,
                    d[c] = i.dataLabel,
                    i.dataLabel = i.dataLabelUpper,
                    i.below = !1,
                    m) {
                        if (!h)
                            f.align = "left";
                        f.x = f.xHigh
                    } else
                        f.y = f.yHigh;
                e.drawDataLabels && e.drawDataLabels.apply(this, arguments);
                for (c = b; c--; )
                    if (i = a[c],
                    i.dataLabelUpper = i.dataLabel,
                    i.dataLabel = d[c],
                    i.y = i.low,
                    i.plotY = i._plotY,
                    i.below = !0,
                    m) {
                        if (!h)
                            f.align = "right";
                        f.x = f.xLow
                    } else
                        f.y = f.yLow;
                e.drawDataLabels && e.drawDataLabels.apply(this, arguments)
            }
            f.align = h
        },
        alignDataLabel: function() {
            g.column.prototype.alignDataLabel.apply(this, arguments)
        },
        setStackedPoints: t,
        getSymbol: t,
        drawPoints: t
    });
    p.areasplinerange = o(p.arearange);
    g.areasplinerange = v(g.arearange, {
        type: "areasplinerange",
        getPointSpline: g.spline.prototype.getPointSpline
    });
    (function() {
        var a = g.column.prototype;
        p.columnrange = o(p.column, p.arearange, {
            lineWidth: 1,
            pointRange: null
        });
        g.columnrange = v(g.arearange, {
            type: "columnrange",
            translate: function() {
                var b = this, c = b.yAxis, d;
                a.translate.apply(b);
                u(b.points, function(a) {
                    var f = a.shapeArgs, h = b.options.minPointLength, i;
                    a.tooltipPos = null;
                    a.plotHigh = d = c.translate(a.high, 0, 1, 0, 1);
                    a.plotLow = a.plotY;
                    i = d;
                    a = a.plotY - d;
                    a < h && (h -= a,
                    a += h,
                    i -= h / 2);
                    f.height = a;
                    f.y = i
                })
            },
            trackerGroups: ["group", "dataLabelsGroup"],
            drawGraph: t,
            pointAttrToOptions: a.pointAttrToOptions,
            drawPoints: a.drawPoints,
            drawTracker: a.drawTracker,
            animate: a.animate,
            getColumnMetrics: a.getColumnMetrics
        })
    }
    )();
    p.gauge = o(p.line, {
        dataLabels: {
            enabled: !0,
            defer: !1,
            y: 15,
            borderWidth: 1,
            borderColor: "silver",
            borderRadius: 3,
            crop: !1,
            verticalAlign: "top",
            zIndex: 2
        },
        dial: {},
        pivot: {},
        tooltip: {
            headerFormat: ""
        },
        showInLegend: !1
    });
    z = {
        type: "gauge",
        pointClass: v(I, {
            setState: function(a) {
                this.state = a
            }
        }),
        angular: !0,
        drawGraph: t,
        fixedBox: !0,
        forceDL: !0,
        trackerGroups: ["group", "dataLabelsGroup"],
        translate: function() {
            var a = this.yAxis
              , b = this.options
              , c = a.center;
            this.generatePoints();
            u(this.points, function(d) {
                var e = o(b.dial, d.dial)
                  , f = x(q(e.radius, 80)) * c[2] / 200
                  , h = x(q(e.baseLength, 70)) * f / 100
                  , i = x(q(e.rearLength, 10)) * f / 100
                  , m = e.baseWidth || 3
                  , l = e.topWidth || 1
                  , j = b.overshoot
                  , n = a.startAngleRad + a.translate(d.y, null, null, null, !0);
                j && typeof j === "number" ? (j = j / 180 * Math.PI,
                n = Math.max(a.startAngleRad - j, Math.min(a.endAngleRad + j, n))) : b.wrap === !1 && (n = Math.max(a.startAngleRad, Math.min(a.endAngleRad, n)));
                n = n * 180 / Math.PI;
                d.shapeType = "path";
                d.shapeArgs = {
                    d: e.path || ["M", -i, -m / 2, "L", h, -m / 2, f, -l / 2, f, l / 2, h, m / 2, -i, m / 2, "z"],
                    translateX: c[0],
                    translateY: c[1],
                    rotation: n
                };
                d.plotX = c[0];
                d.plotY = c[1]
            })
        },
        drawPoints: function() {
            var a = this
              , b = a.yAxis.center
              , c = a.pivot
              , d = a.options
              , e = d.pivot
              , f = a.chart.renderer;
            u(a.points, function(c) {
                var b = c.graphic
                  , e = c.shapeArgs
                  , l = e.d
                  , j = o(d.dial, c.dial);
                b ? (b.animate(e),
                e.d = l) : c.graphic = f[c.shapeType](e).attr({
                    stroke: j.borderColor || "none",
                    "stroke-width": j.borderWidth || 0,
                    fill: j.backgroundColor || "black",
                    rotation: e.rotation
                }).add(a.group)
            });
            c ? c.animate({
                translateX: b[0],
                translateY: b[1]
            }) : a.pivot = f.circle(0, 0, q(e.radius, 5)).attr({
                "stroke-width": e.borderWidth || 0,
                stroke: e.borderColor || "silver",
                fill: e.backgroundColor || "black"
            }).translate(b[0], b[1]).add(a.group)
        },
        animate: function(a) {
            var b = this;
            if (!a)
                u(b.points, function(a) {
                    var d = a.graphic;
                    d && (d.attr({
                        rotation: b.yAxis.startAngleRad * 180 / Math.PI
                    }),
                    d.animate({
                        rotation: a.shapeArgs.rotation
                    }, b.options.animation))
                }),
                b.animate = null
        },
        render: function() {
            this.group = this.plotGroup("group", "series", this.visible ? "visible" : "hidden", this.options.zIndex, this.chart.seriesGroup);
            s.prototype.render.call(this);
            this.group.clip(this.chart.clipRect)
        },
        setData: function(a, b) {
            s.prototype.setData.call(this, a, !1);
            this.processData();
            this.generatePoints();
            q(b, !0) && this.chart.redraw()
        },
        drawTracker: z && z.drawTrackerPoint
    };
    g.gauge = v(g.line, z);
    p.boxplot = o(p.column, {
        fillColor: "#FFFFFF",
        lineWidth: 1,
        medianWidth: 2,
        states: {
            hover: {
                brightness: -0.3
            }
        },
        threshold: null,
        tooltip: {
            pointFormat: '<span style="color:{point.color}">●</span> <b> {series.name}</b><br/>Maximum: {point.high}<br/>Upper quartile: {point.q3}<br/>Median: {point.median}<br/>Lower quartile: {point.q1}<br/>Minimum: {point.low}<br/>'
        },
        whiskerLength: "50%",
        whiskerWidth: 2
    });
    g.boxplot = v(g.column, {
        type: "boxplot",
        pointArrayMap: ["low", "q1", "median", "q3", "high"],
        toYData: function(a) {
            return [a.low, a.q1, a.median, a.q3, a.high]
        },
        pointValKey: "high",
        pointAttrToOptions: {
            fill: "fillColor",
            stroke: "color",
            "stroke-width": "lineWidth"
        },
        drawDataLabels: t,
        translate: function() {
            var a = this.yAxis
              , b = this.pointArrayMap;
            g.column.prototype.translate.apply(this);
            u(this.points, function(c) {
                u(b, function(b) {
                    c[b] !== null && (c[b + "Plot"] = a.translate(c[b], 0, 1, 0, 1))
                })
            })
        },
        drawPoints: function() {
            var a = this, b = a.points, c = a.options, d = a.chart.renderer, e, f, h, i, m, l, j, n, g, A, k, J, p, o, r, t, v, s, w, x, z, y, F = a.doQuartiles !== !1, C = parseInt(a.options.whiskerLength, 10) / 100;
            u(b, function(b) {
                g = b.graphic;
                z = b.shapeArgs;
                k = {};
                o = {};
                t = {};
                y = b.color || a.color;
                if (b.plotY !== D)
                    if (e = b.pointAttr[b.selected ? "selected" : ""],
                    v = z.width,
                    s = B(z.x),
                    w = s + v,
                    x = E(v / 2),
                    f = B(F ? b.q1Plot : b.lowPlot),
                    h = B(F ? b.q3Plot : b.lowPlot),
                    i = B(b.highPlot),
                    m = B(b.lowPlot),
                    k.stroke = b.stemColor || c.stemColor || y,
                    k["stroke-width"] = q(b.stemWidth, c.stemWidth, c.lineWidth),
                    k.dashstyle = b.stemDashStyle || c.stemDashStyle,
                    o.stroke = b.whiskerColor || c.whiskerColor || y,
                    o["stroke-width"] = q(b.whiskerWidth, c.whiskerWidth, c.lineWidth),
                    t.stroke = b.medianColor || c.medianColor || y,
                    t["stroke-width"] = q(b.medianWidth, c.medianWidth, c.lineWidth),
                    j = k["stroke-width"] % 2 / 2,
                    n = s + x + j,
                    A = ["M", n, h, "L", n, i, "M", n, f, "L", n, m],
                    F && (j = e["stroke-width"] % 2 / 2,
                    n = B(n) + j,
                    f = B(f) + j,
                    h = B(h) + j,
                    s += j,
                    w += j,
                    J = ["M", s, h, "L", s, f, "L", w, f, "L", w, h, "L", s, h, "z"]),
                    C && (j = o["stroke-width"] % 2 / 2,
                    i += j,
                    m += j,
                    p = ["M", n - x * C, i, "L", n + x * C, i, "M", n - x * C, m, "L", n + x * C, m]),
                    j = t["stroke-width"] % 2 / 2,
                    l = E(b.medianPlot) + j,
                    r = ["M", s, l, "L", w, l],
                    g)
                        b.stem.animate({
                            d: A
                        }),
                        C && b.whiskers.animate({
                            d: p
                        }),
                        F && b.box.animate({
                            d: J
                        }),
                        b.medianShape.animate({
                            d: r
                        });
                    else {
                        b.graphic = g = d.g().add(a.group);
                        b.stem = d.path(A).attr(k).add(g);
                        if (C)
                            b.whiskers = d.path(p).attr(o).add(g);
                        if (F)
                            b.box = d.path(J).attr(e).add(g);
                        b.medianShape = d.path(r).attr(t).add(g)
                    }
            })
        }
    });
    p.errorbar = o(p.boxplot, {
        color: "#000000",
        grouping: !1,
        linkedTo: ":previous",
        tooltip: {
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.low}</b> - <b>{point.high}</b><br/>'
        },
        whiskerWidth: null
    });
    g.errorbar = v(g.boxplot, {
        type: "errorbar",
        pointArrayMap: ["low", "high"],
        toYData: function(a) {
            return [a.low, a.high]
        },
        pointValKey: "high",
        doQuartiles: !1,
        drawDataLabels: g.arearange ? g.arearange.prototype.drawDataLabels : t,
        getColumnMetrics: function() {
            return this.linkedParent && this.linkedParent.columnMetrics || g.column.prototype.getColumnMetrics.call(this)
        }
    });
    p.waterfall = o(p.column, {
        lineWidth: 1,
        lineColor: "#333",
        dashStyle: "dot",
        borderColor: "#333",
        dataLabels: {
            inside: !0
        },
        states: {
            hover: {
                lineWidthPlus: 0
            }
        }
    });
    g.waterfall = v(g.column, {
        type: "waterfall",
        upColorProp: "fill",
        pointArrayMap: ["low", "y"],
        pointValKey: "y",
        translate: function() {
            var a = this.options, b = this.yAxis, c, d, e, f, h, i, m, l, j, n = a.threshold, k = a.stacking;
            g.column.prototype.translate.apply(this);
            m = l = n;
            d = this.points;
            for (c = 0,
            a = d.length; c < a; c++) {
                e = d[c];
                i = this.processedYData[c];
                f = e.shapeArgs;
                j = (h = k && b.stacks[(this.negStacks && i < n ? "-" : "") + this.stackKey]) ? h[e.x].points[this.index + "," + c] : [0, i];
                if (e.isSum || e.isIntermediateSum)
                    e.y = i;
                h = N(m, m + e.y) + j[0];
                f.y = b.translate(h, 0, 1);
                e.isSum ? (f.y = b.translate(j[1], 0, 1),
                f.height = b.translate(j[0], 0, 1) - f.y) : e.isIntermediateSum ? (f.y = b.translate(j[1], 0, 1),
                f.height = b.translate(l, 0, 1) - f.y,
                l = j[1]) : m += i;
                f.height < 0 && (f.y += f.height,
                f.height *= -1);
                e.plotY = f.y = E(f.y) - this.borderWidth % 2 / 2;
                f.height = N(E(f.height), 0.001);
                e.yBottom = f.y + f.height;
                f = e.plotY + (e.negative ? f.height : 0);
                this.chart.inverted ? e.tooltipPos[0] = b.len - f : e.tooltipPos[1] = f
            }
        },
        processData: function(a) {
            var b = this.yData, c = this.options.data, d, e = b.length, f, h, i, m, l, j;
            h = f = i = m = this.options.threshold || 0;
            for (j = 0; j < e; j++)
                l = b[j],
                d = c && c[j] ? c[j] : {},
                l === "sum" || d.isSum ? b[j] = h : l === "intermediateSum" || d.isIntermediateSum ? b[j] = f : (h += l,
                f += l),
                i = Math.min(h, i),
                m = Math.max(h, m);
            s.prototype.processData.call(this, a);
            this.dataMin = i;
            this.dataMax = m
        },
        toYData: function(a) {
            if (a.isSum)
                return a.x === 0 ? null : "sum";
            else if (a.isIntermediateSum)
                return a.x === 0 ? null : "intermediateSum";
            return a.y
        },
        getAttribs: function() {
            g.column.prototype.getAttribs.apply(this, arguments);
            var a = this
              , b = a.options
              , c = b.states
              , d = b.upColor || a.color
              , b = k.Color(d).brighten(0.1).get()
              , e = o(a.pointAttr)
              , f = a.upColorProp;
            e[""][f] = d;
            e.hover[f] = c.hover.upColor || b;
            e.select[f] = c.select.upColor || d;
            u(a.points, function(b) {
                if (!b.options.color)
                    b.y > 0 ? (b.pointAttr = e,
                    b.color = d) : b.pointAttr = a.pointAttr
            })
        },
        getGraphPath: function() {
            var a = this.data, b = a.length, c = E(this.options.lineWidth + this.borderWidth) % 2 / 2, d = [], e, f, h;
            for (h = 1; h < b; h++)
                f = a[h].shapeArgs,
                e = a[h - 1].shapeArgs,
                f = ["M", e.x + e.width, e.y + c, "L", f.x, e.y + c],
                a[h - 1].y < 0 && (f[2] += e.height,
                f[5] += e.height),
                d = d.concat(f);
            return d
        },
        getExtremes: t,
        drawGraph: s.prototype.drawGraph
    });
    p.polygon = o(p.scatter, {
        marker: {
            enabled: !1
        }
    });
    g.polygon = v(g.scatter, {
        type: "polygon",
        fillGraph: !0,
        getSegmentPath: function(a) {
            return s.prototype.getSegmentPath.call(this, a).concat("z")
        },
        drawGraph: s.prototype.drawGraph,
        drawLegendSymbol: k.LegendSymbolMixin.drawRectangle
    });
    p.bubble = o(p.scatter, {
        dataLabels: {
            formatter: function() {
                return this.point.z
            },
            inside: !0,
            verticalAlign: "middle"
        },
        marker: {
            lineColor: null,
            lineWidth: 1
        },
        minSize: 8,
        maxSize: "20%",
        states: {
            hover: {
                halo: {
                    size: 5
                }
            }
        },
        tooltip: {
            pointFormat: "({point.x}, {point.y}), Size: {point.z}"
        },
        turboThreshold: 0,
        zThreshold: 0,
        zoneAxis: "z"
    });
    z = v(I, {
        haloPath: function() {
            return I.prototype.haloPath.call(this, this.shapeArgs.r + this.series.options.states.hover.halo.size)
        },
        ttBelow: !1
    });
    g.bubble = v(g.scatter, {
        type: "bubble",
        pointClass: z,
        pointArrayMap: ["y", "z"],
        parallelArrays: ["x", "y", "z"],
        trackerGroups: ["group", "dataLabelsGroup"],
        bubblePadding: !0,
        zoneAxis: "z",
        pointAttrToOptions: {
            stroke: "lineColor",
            "stroke-width": "lineWidth",
            fill: "fillColor"
        },
        applyOpacity: function(a) {
            var b = this.options.marker
              , c = q(b.fillOpacity, 0.5)
              , a = a || b.fillColor || this.color;
            c !== 1 && (a = U(a).setOpacity(c).get("rgba"));
            return a
        },
        convertAttribs: function() {
            var a = s.prototype.convertAttribs.apply(this, arguments);
            a.fill = this.applyOpacity(a.fill);
            return a
        },
        getRadii: function(a, b, c, d) {
            var e, f, h, i = this.zData, m = [], l = this.options.sizeBy !== "width";
            for (f = 0,
            e = i.length; f < e; f++)
                h = b - a,
                h = h > 0 ? (i[f] - a) / (b - a) : 0.5,
                l && h >= 0 && (h = Math.sqrt(h)),
                m.push(w.ceil(c + h * (d - c)) / 2);
            this.radii = m
        },
        animate: function(a) {
            var b = this.options.animation;
            if (!a)
                u(this.points, function(a) {
                    var d = a.graphic
                      , a = a.shapeArgs;
                    d && a && (d.attr("r", 1),
                    d.animate({
                        r: a.r
                    }, b))
                }),
                this.animate = null
        },
        translate: function() {
            var a, b = this.data, c, d, e = this.radii;
            g.scatter.prototype.translate.call(this);
            for (a = b.length; a--; )
                c = b[a],
                d = e ? e[a] : 0,
                d >= this.minPxSize / 2 ? (c.shapeType = "circle",
                c.shapeArgs = {
                    x: c.plotX,
                    y: c.plotY,
                    r: d
                },
                c.dlBox = {
                    x: c.plotX - d,
                    y: c.plotY - d,
                    width: 2 * d,
                    height: 2 * d
                }) : c.shapeArgs = c.plotY = c.dlBox = D
        },
        drawLegendSymbol: function(a, b) {
            var c = x(a.itemStyle.fontSize) / 2;
            b.legendSymbol = this.chart.renderer.circle(c, a.baseline - c, c).attr({
                zIndex: 3
            }).add(b.legendGroup);
            b.legendSymbol.isMarker = !0
        },
        drawPoints: g.column.prototype.drawPoints,
        alignDataLabel: g.column.prototype.alignDataLabel,
        buildKDTree: t,
        applyZones: t
    });
    M.prototype.beforePadding = function() {
        var a = this
          , b = this.len
          , c = this.chart
          , d = 0
          , e = b
          , f = this.isXAxis
          , h = f ? "xData" : "yData"
          , i = this.min
          , m = {}
          , l = w.min(c.plotWidth, c.plotHeight)
          , j = Number.MAX_VALUE
          , n = -Number.MAX_VALUE
          , g = this.max - i
          , k = b / g
          , p = [];
        u(this.series, function(b) {
            var h = b.options;
            if (b.bubblePadding && (b.visible || !c.options.chart.ignoreHiddenSeries))
                if (a.allowZoomOutside = !0,
                p.push(b),
                f)
                    u(["minSize", "maxSize"], function(a) {
                        var b = h[a]
                          , f = /%$/.test(b)
                          , b = x(b);
                        m[a] = f ? l * b / 100 : b
                    }),
                    b.minPxSize = m.minSize,
                    b = b.zData,
                    b.length && (j = q(h.zMin, w.min(j, w.max(P(b), h.displayNegative === !1 ? h.zThreshold : -Number.MAX_VALUE))),
                    n = q(h.zMax, w.max(n, Q(b))))
        });
        u(p, function(a) {
            var b = a[h], c = b.length, l;
            f && a.getRadii(j, n, m.minSize, m.maxSize);
            if (g > 0)
                for (; c--; )
                    typeof b[c] === "number" && (l = a.radii[c],
                    d = Math.min((b[c] - i) * k - l, d),
                    e = Math.max((b[c] - i) * k + l, e))
        });
        p.length && g > 0 && q(this.options.min, this.userMin) === D && q(this.options.max, this.userMax) === D && (e -= b,
        k *= (b + d - e) / b,
        this.min += d / k,
        this.max += e / k)
    }
    ;
    (function() {
        function a(a, b, c) {
            a.call(this, b, c);
            if (this.chart.polar)
                this.closeSegment = function(a) {
                    var b = this.xAxis.center;
                    a.push("L", b[0], b[1])
                }
                ,
                this.closedStacks = !0
        }
        function b(a, b) {
            var c = this.chart
              , d = this.options.animation
              , e = this.group
              , j = this.markerGroup
              , n = this.xAxis.center
              , g = c.plotLeft
              , k = c.plotTop;
            if (c.polar) {
                if (c.renderer.isSVG)
                    d === !0 && (d = {}),
                    b ? (c = {
                        translateX: n[0] + g,
                        translateY: n[1] + k,
                        scaleX: 0.001,
                        scaleY: 0.001
                    },
                    e.attr(c),
                    j && j.attr(c)) : (c = {
                        translateX: g,
                        translateY: k,
                        scaleX: 1,
                        scaleY: 1
                    },
                    e.animate(c, d),
                    j && j.animate(c, d),
                    this.animate = null)
            } else
                a.call(this, b)
        }
        var c = s.prototype, d = S.prototype, e;
        c.searchPolarPoint = function(a) {
            var b = this.chart
              , c = this.xAxis.pane.center
              , d = a.chartX - c[0] - b.plotLeft
              , a = a.chartY - c[1] - b.plotTop;
            this.kdAxisArray = ["clientX"];
            a = {
                clientX: 180 + Math.atan2(d, a) * (-180 / Math.PI)
            };
            return this.searchKDTree(a)
        }
        ;
        r(c, "buildKDTree", function(a) {
            if (this.chart.polar)
                this.kdAxisArray = ["clientX"];
            a.apply(this)
        });
        r(c, "searchPoint", function(a, b) {
            return this.chart.polar ? this.searchPolarPoint(b) : a.call(this, b)
        });
        c.toXY = function(a) {
            var b, c = this.chart, d = a.plotX;
            b = a.plotY;
            a.rectPlotX = d;
            a.rectPlotY = b;
            d = (d / Math.PI * 180 + this.xAxis.pane.options.startAngle) % 360;
            d < 0 && (d += 360);
            a.clientX = d;
            b = this.xAxis.postTranslate(a.plotX, this.yAxis.len - b);
            a.plotX = a.polarPlotX = b.x - c.plotLeft;
            a.plotY = a.polarPlotY = b.y - c.plotTop
        }
        ;
        g.area && r(g.area.prototype, "init", a);
        g.areaspline && r(g.areaspline.prototype, "init", a);
        g.spline && r(g.spline.prototype, "getPointSpline", function(a, b, c, d) {
            var e, j, n, g, k, p, o;
            if (this.chart.polar) {
                e = c.plotX;
                j = c.plotY;
                a = b[d - 1];
                n = b[d + 1];
                this.connectEnds && (a || (a = b[b.length - 2]),
                n || (n = b[1]));
                if (a && n)
                    g = a.plotX,
                    k = a.plotY,
                    b = n.plotX,
                    p = n.plotY,
                    g = (1.5 * e + g) / 2.5,
                    k = (1.5 * j + k) / 2.5,
                    n = (1.5 * e + b) / 2.5,
                    o = (1.5 * j + p) / 2.5,
                    b = Math.sqrt(Math.pow(g - e, 2) + Math.pow(k - j, 2)),
                    p = Math.sqrt(Math.pow(n - e, 2) + Math.pow(o - j, 2)),
                    g = Math.atan2(k - j, g - e),
                    k = Math.atan2(o - j, n - e),
                    o = Math.PI / 2 + (g + k) / 2,
                    Math.abs(g - o) > Math.PI / 2 && (o -= Math.PI),
                    g = e + Math.cos(o) * b,
                    k = j + Math.sin(o) * b,
                    n = e + Math.cos(Math.PI + o) * p,
                    o = j + Math.sin(Math.PI + o) * p,
                    c.rightContX = n,
                    c.rightContY = o;
                d ? (c = ["C", a.rightContX || a.plotX, a.rightContY || a.plotY, g || e, k || j, e, j],
                a.rightContX = a.rightContY = null) : c = ["M", e, j]
            } else
                c = a.call(this, b, c, d);
            return c
        });
        r(c, "translate", function(a) {
            a.call(this);
            if (this.chart.polar && !this.preventPostTranslate)
                for (var a = this.points, b = a.length; b--; )
                    this.toXY(a[b])
        });
        r(c, "getSegmentPath", function(a, b) {
            var c = this.points;
            if (this.chart.polar && this.options.connectEnds !== !1 && b[b.length - 1] === c[c.length - 1] && c[0].y !== null)
                this.connectEnds = !0,
                b = [].concat(b, [c[0]]);
            return a.call(this, b)
        });
        r(c, "animate", b);
        if (g.column)
            e = g.column.prototype,
            r(e, "animate", b),
            r(e, "translate", function(a) {
                var b = this.xAxis, c = this.yAxis.len, d = b.center, e = b.startAngleRad, j = this.chart.renderer, g, k;
                this.preventPostTranslate = !0;
                a.call(this);
                if (b.isRadial) {
                    b = this.points;
                    for (k = b.length; k--; )
                        g = b[k],
                        a = g.barX + e,
                        g.shapeType = "path",
                        g.shapeArgs = {
                            d: j.symbols.arc(d[0], d[1], c - g.plotY, null, {
                                start: a,
                                end: a + g.pointWidth,
                                innerR: c - q(g.yBottom, c)
                            })
                        },
                        this.toXY(g),
                        g.tooltipPos = [g.plotX, g.plotY],
                        g.ttBelow = g.plotY > d[1]
                }
            }),
            r(e, "alignDataLabel", function(a, b, d, e, g, j) {
                if (this.chart.polar) {
                    a = b.rectPlotX / Math.PI * 180;
                    if (e.align === null)
                        e.align = a > 20 && a < 160 ? "left" : a > 200 && a < 340 ? "right" : "center";
                    if (e.verticalAlign === null)
                        e.verticalAlign = a < 45 || a > 315 ? "bottom" : a > 135 && a < 225 ? "top" : "middle";
                    c.alignDataLabel.call(this, b, d, e, g, j)
                } else
                    a.call(this, b, d, e, g, j)
            });
        r(d, "getCoordinates", function(a, b) {
            var c = this.chart
              , d = {
                xAxis: [],
                yAxis: []
            };
            c.polar ? u(c.axes, function(a) {
                var e = a.isXAxis
                  , f = a.center
                  , g = b.chartX - f[0] - c.plotLeft
                  , f = b.chartY - f[1] - c.plotTop;
                d[e ? "xAxis" : "yAxis"].push({
                    axis: a,
                    value: a.translate(e ? Math.PI - Math.atan2(g, f) : Math.sqrt(Math.pow(g, 2) + Math.pow(f, 2)), !0)
                })
            }) : d = a.call(this, b);
            return d
        })
    }
    )()
}
)(Highcharts);
