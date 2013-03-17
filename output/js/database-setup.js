var DEMODB;

function errorHandler(transaction, error)
{
    "use strict";

    if(error.code === 1)
    {
        // DB Table already exists
    }
    else
    {
        // Error is a human-readable string.
        console.log('Oops.  Error was ' + error.message + ' (Code ' + error.code + ')');
    }
    return false;
}

function dataSelectHandler(transaction, results)
{
    // Handle the results
    for(var i = 0; i < results.rows.length; i++)
    {

        var row = results.rows.item(i);
        $("#placeholder1").append("<p><a href='http://gatherer.wizards.com/pages/card/Details.aspx?multiverseid=" + row.id + "' target='_blank'>" + (i + 1) + ". " + row.name + "</a> " + row.rating + "</p>");
    }
}

function nullDataHandler()
{
    console.log("SQL Query Succeeded");
}

function createTables(data)
{
    "use strict";

    var createTablesRequest = function(transaction)
    {
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_names(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL);', [], nullDataHandler, errorHandler);
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_expansion(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL);', [], nullDataHandler, errorHandler);
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_rating(id INTEGER NOT NULL PRIMARY KEY, rating INTEGER NOT NULL);', [], nullDataHandler, errorHandler);
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_image(id INTEGER NOT NULL PRIMARY KEY, file TEXT NOT NULL);', [], nullDataHandler, errorHandler);
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_artist(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL);', [], nullDataHandler, errorHandler);
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_rarity(id INTEGER NOT NULL PRIMARY KEY, rarity TEXT NOT NULL);', [], nullDataHandler, errorHandler);
        transaction.executeSql('CREATE TABLE IF NOT EXISTS card_prices(id INTEGER NOT NULL PRIMARY KEY, price INTEGER NOT NULL);', [], nullDataHandler, errorHandler);
    };
    DEMODB.transaction(createTablesRequest);
    prePopulate(data);
}

function prePopulate(data)
{
    "use strict";

    var insertContents = function(transaction)
    {
        console.log("Inserting contents");
        var len = data.length;
        for(var i = 0; i < len; i++)
        {
            console.log("Inserting contents #" + i);
            transaction.executeSql("INSERT INTO card_names(id, name) VALUES (?, ?)", [parseInt(data[i].uid, 10), data[i].cardname]);
            transaction.executeSql("INSERT INTO card_expansion(id, name) VALUES (?, ?)", [parseInt(data[i].uid, 10), data[i].expansion]);
            transaction.executeSql("INSERT INTO card_rating(id, rating) VALUES (?, ?)", [parseInt(data[i].uid, 10), parseFloat(data[i].rating, 10)]);
            for(var j = 0; j < data[i].images.length; j++)
            {
                if(data[i].images[j] !== "")
                {
                    transaction.executeSql("INSERT INTO card_image(id, file) VALUES (?, ?)", [parseInt(data[i].uid, 10), data[i].images[j]]);
                }
            }
            transaction.executeSql("INSERT INTO card_artist(id, name) VALUES (?, ?)", [parseInt(data[i].uid, 10), data[i].name]);
            transaction.executeSql("INSERT INTO card_rarity(id, rarity) VALUES (?, ?)", [parseInt(data[i].uid, 10), data[i].rarity]);
            for(var j = 0; j < data[i].prices.length; j++)
            {
                if(data[i].prices[j] !== "")
                {
                    transaction.executeSql("INSERT INTO card_prices(id, price) VALUES (?, ?)", [parseInt(data[i].uid, 10), parseFloat(data[i].prices[j], 10)]);
                }
            }
        }
        console.log("Content insert complete.");
        //Optional Starter Data when page is initialized
//        var data = ['1', 'none', '#B3B4EF', 'Helvetica', 'Porsche 911 GT3'];
//        transaction.executeSql("INSERT INTO page_settings(id, fname, bgcolor, font, favcar) VALUES (?, ?, ?, ?, ?)", [data[0], data[1], data[2], data[3], data[4]]);
    };
    DEMODB.transaction(insertContents);
}

function selectAll()
{
    "use strict";

    var selectFromDB = function(transaction)
    {
        transaction.executeSql("SELECT * FROM card_names JOIN card_rating ON card_rating.id = card_names.id WHERE card_names.id IN (SELECT card_rating.id FROM card_rating ORDER BY card_rating.rating DESC LIMIT 50) ORDER BY card_rating.rating DESC;", [], dataSelectHandler, errorHandler);
    };
    DEMODB.transaction(selectFromDB);
}

function initDatabase(data)
{
    "use strict";

    try
    {
        if(!window.openDatabase)
        {
            alert('Databases are not supported in this browser.');
        }
        else
        {
            var shortName = 'MTG_DB_4';
            var version = '0.3';
            var displayName = 'MTG Cards Database';
            var maxSize = 100000; //  bytes
            DEMODB = openDatabase(shortName, version, displayName, maxSize);
            createTables(data);
            selectAll();
        }
    }
    catch(e)
    {
        if(e === 2)
        {
            // Version number mismatch.
            console.log("Invalid database version.");
        }
        else
        {
            console.log("Unknown error " + e + ".");
        }
        return;
    }
}