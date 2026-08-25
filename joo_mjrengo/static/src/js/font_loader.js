/**
 * Font Loader for joo_mjrengo
 *
 * This module loads the configured font from the server
 * and dynamically injects a CSS rule that updates the
 * `.joo-font` class. Other modules can simply use this class
 * without knowing which font is selected.
 */

odoo.define('joo_mjrengo.font_loader', function (require) {
    'use strict';

    const ajax = require('web.ajax');

    // Mapping between configuration keys and actual font-family names
    const FONT_MAP = {
        ipamjm: 'IPAmjMincho',
        dwpimincho: 'DWPIMincho',
        dwpiexmincho: 'DWPIexMincho',
    };

    /**
     * Fetch selected font from server and apply CSS.
     */
    ajax.rpc('/joo_mjrengo/font')
        .then(function (fontKey) {
            const fontFamily = FONT_MAP[fontKey] || null;

            if (!fontFamily) {
                console.warn(
                    '[joo_mjrengo] Unknown font key received:',
                    fontKey
                );
                return;
            }

            const css = `.joo-font { font-family: "${fontFamily}", serif !important; }`;

            const style = document.createElement('style');
            style.innerHTML = css;
            document.head.appendChild(style);

            console.debug('[joo_mjrengo] Applied font:', fontFamily);
        })
        .catch(function (err) {
            console.error('[joo_mjrengo] Failed to load font configuration:', err);
        });
});
