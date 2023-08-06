function addRemoveElement(toChangeID, buttonID, description, plusMinusOptions)
{
    if (plusMinusOptions)
    {
        hideValue = plusMinusOptions.split('|')[0]        
        showValue = plusMinusOptions.split('|')[1]
    }
    else
    {
        hideValue = '-'        
        showValue = '+'
    }

    var plusOrMinus = document.getElementById(buttonID).innerHTML;
    if(plusOrMinus==showValue)
    {
        document.getElementById(buttonID).innerHTML = hideValue;
        document.getElementById(toChangeID).style.display="block";
        document.getElementById(toChangeID).style.visibility="visible";
        document.getElementById(buttonID).title = 'hide ' + description;
    }
    else
    {
        document.getElementById(buttonID).innerHTML = showValue;
        document.getElementById(buttonID).title = 'show ' + description;
        document.getElementById(toChangeID).style.display="none";
    }
}

function confirmDelete(entityType, entityID)
{
    var decision = confirm('Are you sure you want to delete ' + entityType + ' ' + entityID + '?');
    if (decision)
        return true;
    else
        return false;
}
