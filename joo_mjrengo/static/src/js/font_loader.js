odoo.define('joo_mjrengo.font_loader', function (require) {
    const ajax = require('web.ajax');

    ajax.rpc('/joo_mjrengo/font').then(function (font) {
        let css = '';

        if (font === 'ipamjm') {
            css = `.joo-font { font-family: "IPAmjMincho", serif !important; }`;
        } else if (font === 'dwpimincho') {
            css = `.joo-font { font-family: "DWPIMincho", serif !important; }`;
        } else if (font === 'dwpiexmincho') {
            css = `.joo-font { font-family: "DWPIexMincho", serif !important; }`;
        }

        const style = document.createElement('style');
        style.innerHTML = css;
        document.head.appendChild(style);
    });
});
