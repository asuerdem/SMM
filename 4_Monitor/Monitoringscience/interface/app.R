library(shiny)
# library(DBI)
# source("Transform.R")

# setwd("~/../Dropbox/BloombergToFuat/Datasource_project/controlPanel/tablepanel/")
# conn        <- dbConnect(drv = RSQLite::SQLite(),dbname = "littlebig2.db")
# rs          <- dbSendQuery(conn, 'SELECT * FROM Main_Data')
# indicesList <- colnames(dbFetch(rs))[-(1:3)]
# dbClearResult(rs)
# dbDisconnect(conn)

corpora_list <- c("AI","Biotechnology")

ui <- fluidPage(
  fluidRow(
    column(12,titlePanel("Monitoring Science")),
    column(12,sliderInput("sliderYear", "Select Year Range",sep = "",
                1990, 2015, value = c(2000, 2015))),
    column(12, offset = 0, style='padding:12px;'),
    column(12,
           column(12,column(4,selectInput('columns', 'Select columns', c("Select columns",corpora_list), multiple=F, selectize=T))),
           column(12,column(4,selectInput('corpus', 'Select corpus', c("Select corpus",corpora_list), multiple=F, selectize=T))),
           column(12,column(4,textInput('addwords', 'Add word(s)',placeholder = "Separate with  \",\"" ))),
           # column(12,column(4,textInput("table_name","Output file name"))),
           column(12,column(4,submitButton("Show Table"))),
           column(12, offset = 0, style='padding:7px;'),
           column(12,column(3,downloadButton('writecsv', 'Save data table to .csv'))
                  # column(3,downloadButton('writexlsx', 'Save data table to .xlsx'))
           ),
           column(12, offset = 0, style='padding:7px;'),
           h3("Table"),
           column(12,tableOutput("table"))
           
    )
    
  ) #end fluidrow
)  ### Fluid page end 


#### Initiate shinyServer
server <- function(input, output) {
  
  
  calledData <- reactive({
    if(input$indicators == "Select indicator") stop ("Please select one indicator")
    indDat <- transform(input$corpus)
    
    indDat
  })
  dtableInput <- reactive({
    if(is.null(calledData())) return()
    datas <- calledData()   
    datas
  })
  
  output$table <- renderTable({dtableInput()})
  
  output$writecsv <- downloadHandler(        #### called from UI
    filename = function() {paste("report-", Sys.Date(), ".csv", sep="")},
    content = function(file) {
      write.csv(dtableInput(), file)
    }
  )
  output$writeexcel <- downloadHandler(        #### called from UI
    filename = function() {paste("report-", Sys.Date(), '.xlsx', sep='')},
    content = function(file) {
      xlsx::write.xlsx(dtableInput(),file)
    }
  )
}

shinyApp(ui, server)