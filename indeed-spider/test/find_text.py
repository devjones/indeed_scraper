import lxml
from lxml import html



def main():
  # OPen and load contents of jobfile.txt
  f = open('jobfile.txt', 'r')
  contents = f.read()
  f.close()



  root = html.document_fromstring(contents)
  target_element = None


  # For some reason the summary will not match the lxml extracted text, figure out why
  # This solution is hacky
  import pdb
  pdb.set_trace()

  summary = "Very strong Perl/Shell scripting skills"

  counter  = 0
  for element in root.iter():
    counter += 1
    if element.text:
      if (summary in element.text):
        target_element = element
        print 'YES. element.txt'
        break
    elif element.tail:
      if (summary in element.tail):
        target_element = element
        print 'YES element.tail'
        break

  print counter, ' elements'
  print target_element.tag

if __name__ == '__main__':
  main()
