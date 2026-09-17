%% exam.cls — đề thi Toán THPT (XeLaTeX, tiếng Việt)
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{exam}[2026/09/17 De thi Toan THPT]

\LoadClass[12pt,a4paper]{article}

\RequirePackage{iftex}
\iftutex\else
  \ClassError{exam}{Can bien dich bang XeLaTeX (hoac LuaLaTeX)}{Dung: latexmk -xelatex hoac xelatex}
\fi

\RequirePackage[top=1.0cm,bottom=1.6cm,left=1.8cm,right=1.8cm]{geometry}
\RequirePackage{fontspec}
\RequirePackage{amsmath,amssymb,amsfonts}
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\RequirePackage{array,tabularx}
\RequirePackage{setspace}

% Vietnamese text: Times New Roman on school machines, Liberation Serif on Linux.
\defaultfontfeatures{Ligatures=TeX,Scale=MatchLowercase}
\IfFontExistsTF{Times New Roman}{
  \setmainfont{Times New Roman}[Scale=1.0]
}{
  \IfFontExistsTF{Liberation Serif}{
    \setmainfont{Liberation Serif}[Scale=1.0]
  }{
    \setmainfont{DejaVu Serif}[Scale=1.0]
  }
}
\IfFontExistsTF{Liberation Sans}{
  \setsansfont{Liberation Sans}
}{
  \IfFontExistsTF{Arial}{
    \setsansfont{Arial}
  }{
    \setsansfont{DejaVu Sans}
  }
}
\IfFontExistsTF{Courier New}{
  \setmonofont{Courier New}[Scale=0.92]
}{
  \IfFontExistsTF{Liberation Mono}{
    \setmonofont{Liberation Mono}[Scale=0.92]
  }{
    \setmonofont{DejaVu Sans Mono}[Scale=0.92]
  }
}

\setstretch{1.08}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.22em}
\pagestyle{plain}
\setcounter{secnumdepth}{0}

% ----- metadata -----
\newcommand{\@school}{}
\newcommand{\@department}{}
\newcommand{\@teacher}{}
\newcommand{\@topic}{}
\newcommand{\@examtitle}{ĐỀ KIỂM TRA}
\newcommand{\@subject}{Toán}
\newcommand{\@grade}{}
\newcommand{\@duration}{90 phút}
\newcommand{\@examdate}{}
\newcommand{\school}[1]{\renewcommand{\@school}{#1}}
\newcommand{\department}[1]{\renewcommand{\@department}{#1}}
\newcommand{\teacher}[1]{\renewcommand{\@teacher}{#1}}
\newcommand{\topic}[1]{\renewcommand{\@topic}{#1}}
\newcommand{\examtitle}[1]{\renewcommand{\@examtitle}{#1}}
\newcommand{\subject}[1]{\renewcommand{\@subject}{#1}}
\newcommand{\grade}[1]{\renewcommand{\@grade}{#1}}
\newcommand{\duration}[1]{\renewcommand{\@duration}{#1}}
\newcommand{\examdate}[1]{\renewcommand{\@examdate}{#1}}

% Answer-key toggle: \answerkeytrue / \answerkeyfalse
\newif\ifanswerkey
\answerkeyfalse

% ----- header -----
\def\@examblank{}
\newcommand{\ifexamblank}[3]{%
  \edef\@examchk{#1}%
  \ifx\@examchk\@examblank #2\else #3\fi
}
\newcommand{\makeheader}{%
  \thispagestyle{plain}%
  \ifexamblank{\@department}{%
    \ifexamblank{\@school}{}{%
      \noindent{\centering\fontsize{11}{13}\selectfont\bfseries\@school\par}%
      \vspace{0.15em}%
    }%
  }{%
    \noindent
    \begin{tabularx}{\textwidth}{@{}>{\centering\arraybackslash}X@{\hspace{0.8em}}>{\centering\arraybackslash}X@{}}
      {\fontsize{11}{13}\selectfont\bfseries\@department}\\[0.12em]
      \ifexamblank{\@school}{}{{\fontsize{12}{14}\selectfont\bfseries\@school}}
      &
    \end{tabularx}
    \vspace{0.15em}
  }%
  \begin{center}
    {\fontsize{13}{15}\selectfont\bfseries\@examtitle}\\[0.18em]
    {\fontsize{11}{13}\selectfont\bfseries Môn: \@subject
      \ifx\@grade\empty\else\ -- Lớp \@grade\fi}\\[0.08em]
    \ifexamblank{\@topic}{}{%
      {\fontsize{10}{12}\selectfont Chuyên đề: \@topic}\\[0.08em]
    }%
    {\footnotesize Thời gian làm bài: \@duration\ (không kể thời gian phát đề)%
      \ifexamblank{\@examdate}{}{ \ --\ Ngày kiểm tra: \@examdate}}\\[0.05em]
    {\footnotesize\textit{(Đề thi gồm \arabic{questiontotal} câu)}}
  \end{center}

  \vspace{0.2em}
  \noindent\rule{\textwidth}{0.6pt}\\[-0.12em]
  \noindent\rule{\textwidth}{0.25pt}

  \vspace{0.25em}
  \noindent
  \begin{tabularx}{\textwidth}{@{}X r@{}}
    Họ và tên: \dotfill & Số báo danh: \makebox[3.2cm]{\dotfill}\\[0.32em]
    Lớp: \makebox[3.6cm]{\dotfill} &
    \ifexamblank{\@teacher}{%
      Chữ ký GT: \makebox[3.2cm]{\dotfill}%
    }{%
      {\footnotesize Giáo viên: \@teacher}%
    }
  \end{tabularx}

  \ifanswerkey
    \vspace{0.3em}
    \noindent{\color{red!70!black}\bfseries ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI}
    \par
  \fi
  \vspace{0.18em}
}

% Total question count (set by generator; fallback = last question number)
\newcounter{questiontotal}
\newcommand{\setquestiontotal}[1]{\setcounter{questiontotal}{#1}}

% ----- question / answer environments -----
\newcounter{question}
\renewcommand{\thequestion}{\arabic{question}}

\newenvironment{question}{%
  \par\addvspace{0.28em}%
  \pagebreak[2]%
  \refstepcounter{question}%
  \noindent\textbf{Câu \thequestion.}\hspace{0.4em}\ignorespaces
}{%
  \par\addvspace{0.04em}%
}

\newenvironment{dapan}{%
  \ifanswerkey
    \par\vspace{0.25em}%
    \noindent{\color{blue!60!black}\itshape Đáp án:}\hspace{0.35em}\ignorespaces
  \else
    \setbox0=\vbox\bgroup\color{white}%
  \fi
}{%
  \ifanswerkey
    \par
  \else
    \egroup
  \fi
}

\newenvironment{loigiai}{%
  \ifanswerkey
    \par\vspace{0.2em}%
    \noindent{\small\bfseries Lời giải.}\\[0.15em]
    \begingroup\small
  \else
    \setbox0=\vbox\bgroup\color{white}%
  \fi
}{%
  \ifanswerkey
    \endgroup\par
  \else
    \egroup
  \fi
}

% ABCD 2×2. Dùng \choiceA..\choiceD hoặc \begin{fourchoices}\item..\end{fourchoices}
\newcommand{\choicegrid}[4]{%
  \nopagebreak\vspace{0.08em}%
  \noindent
  \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X@{\hspace{1.2em}}>{\raggedright\arraybackslash}X@{}}
    \textbf{A.} #1 & \textbf{B.} #2 \\[0.12em]
    \textbf{C.} #3 & \textbf{D.} #4
  \end{tabularx}%
  \par
}
\newcounter{choiceitem}
\newenvironment{fourchoices}{%
  \par\addvspace{0.12em}%
  \setcounter{choiceitem}{0}%
  \def\item{%
    \stepcounter{choiceitem}%
    \ifcase\value{choiceitem}%
    \or \noindent\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X@{\hspace{1.2em}}>{\raggedright\arraybackslash}X@{}}%
      \textbf{A.}\hspace{0.35em}\ignorespaces
    \or &\textbf{B.}\hspace{0.35em}\ignorespaces
    \or \\[0.2em]\textbf{C.}\hspace{0.35em}\ignorespaces
    \or &\textbf{D.}\hspace{0.35em}\ignorespaces
    \fi
  }%
}{%
  \end{tabularx}\par
}

\endinput
