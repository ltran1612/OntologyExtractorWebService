curl -X POST -H "Content-Type: application/json" \
http://127.0.0.1:3000/extract -o truncated.owl \
-d @- << EOF

{
"sparql": "
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cpsf: <http://www.asklab.tk/ontologies/CPS-Framework#>

select ?superclass where { 
  ?superclass cpsf:includesConcern* cpsf:Human_Safety
}
"
} 

