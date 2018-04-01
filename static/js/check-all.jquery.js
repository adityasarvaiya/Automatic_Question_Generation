
/*----------------------------------------------------  
    CheckAll plugin for jQuery
    Version: 1.4

    Copyright (c) 2012 Matt Ball
    https://github.com/mjball/jQuery-CheckAll
    April 2, 2012
	
    Requires: jQuery 1.4.2+
    Last tested with: 1.4.4, 1.5.2, 1.6, 1.7.1
------------------------------------------------------*/

;(function($)
{
    $.fn.checkAll = function (group, options)
    {
        var opts = $.extend({}, $.fn.checkAll.defaults, options),
            $master = this,
        
            $slaves = $(group),
            selector,
            groupSize,
            onClick = typeof opts.onClick === 'function' ? opts.onClick : null,
            onMasterClick = typeof opts.onMasterClick === 'function' ? opts.onMasterClick : null,
            reportTo = typeof opts.reportTo === 'function' ? opts.reportTo : null,
            
            // for compatibility with 1.4.2 through 1.6
            propFn = typeof $.fn.prop === 'function' ? 'prop' : 'attr';
        
        // omit the master if it was accidentally selected with the slaves
        if ($slaves.index($master) === -1)
        {
            selector = $slaves.selector;
        }
        else    
        {
            $slaves = $slaves.not($master.selector);
            selector = $slaves.selector.replace('.not(', ':not(');
        }
        
        groupSize = $slaves.length;
        
        if (groupSize === 0)
        {
            // this is kind of a problem
            groupSize = -1;
        }
        
        function _countChecked()
        {
            return $slaves.filter(':checked').length;
        }
            
        function _autoEnable()
        {
            var numChecked = _countChecked();
            $master[propFn]('checked', groupSize === numChecked);
            if (reportTo)
            {
                reportTo(numChecked);
            }
        }
            
        function _autoDisable()
        {
            $master[propFn]('checked', false);
            if (reportTo)
            {
                reportTo(_countChecked());
            }
        }
        
        $master.unbind('click.checkAll').bind('click.checkAll', function (e)
        {
            var check_val = e.target.checked;
            $slaves.add($master)[propFn]('checked', check_val);
            
            if (onMasterClick)
            {
                onMasterClick.apply(this);
            }
            
            if (reportTo)
            {
                reportTo(check_val ? _countChecked() : 0);
            }
        });

        
        if (opts.sync)
        {
            $(selector).die('click.checkAll').live('click.checkAll', function ()
            {
                this.checked ? _autoEnable() : _autoDisable();
                
                if (onClick)
                {
                    onClick.apply(this);
                }
            });
        }
        
        _autoEnable();
        
        return this;
    };
    
    $.fn.checkAll.defaults = {sync: true};
}(jQuery));