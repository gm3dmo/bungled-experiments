#Generates an HTML file of an nmap scan against a target

# Setup some variables:
d=$(date +%s)

# Enter a hostname here or 'lab.3cbeta.co.uk' or some other.
site_to_scan=$1

xml_output_file=xml/nmap.${site_to_scan}.${d}.xml
html_output_file=html/nmap.${site_to_scan}.${d}.html

# Make the output xml and html directories:
for dir in xml html
do
 if [ ! -d ${dir} ]; then
   mkdir ${dir}
 fi
done

# Get the xsl file for nmap off the nmap website:
# You need to be internet accessible for this bit
# but you could download the file and put it in place
xsl_file=nmap.xsl
curl https://svn.nmap.org/nmap/docs/${xsl_file} -o ${xsl_file}

# Run the nmap scan against the target and generate the output in
# XML format using the specified stylesheet.
nmap -oX ${xml_output_file}        \
     --stylesheet ../${xsl_file}   \
     ${site_to_scan}

# Process the xml into the html
xsltproc ${xml_output_file} -o ${html_output_file}

